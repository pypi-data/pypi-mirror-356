import logging
from pathlib import Path
from typing import IO, Any, AsyncGenerator, Generator, Optional, Type, Union, cast

import pydantic
from pydantic import BaseModel

from pyhub.llm.base import BaseLLM
from pyhub.llm.settings import llm_settings
from pyhub.llm.types import (
    Embed,
    EmbedList,
    ImageReply,
    Message,
    OpenAIChatModelType,
    OpenAIEmbeddingModelType,
    Reply,
    Usage,
)
from pyhub.llm.utils.files import IOType, encode_files
from pyhub.llm.utils.templates import Template

logger = logging.getLogger(__name__)


class OpenAIMixin:
    cache_alias = "openai"
    supports_stream_options = True  # Override in subclasses if not supported

    def _make_request_params(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: OpenAIChatModelType,
        use_files: bool = True,
    ) -> dict:
        """OpenAI API 요청에 필요한 파라미터를 준비하고 시스템 프롬프트를 처리합니다."""
        message_history = [dict(message) for message in messages]
        system_prompt = self.get_system_prompt(input_context)

        # choices가 있으면 시스템 프롬프트에 지시사항 추가
        if "choices" in input_context:
            # choices를 보여주고 인덱스로 선택하도록 지시
            choices = input_context["choices"]
            choices_list = "\n".join([f"{i}: {choice}" for i, choice in enumerate(choices)])
            choices_instruction = (
                f"You must select one option from the following choices by returning both the choice text and its zero-based index:\n{choices_list}\n"
                f"Return your selection as JSON with 'choice' (exact text from options), 'choice_index' (the zero-based index), and 'confidence' (0.0-1.0)."
            )
            if input_context.get("allow_none"):
                choices_instruction += "\nIf none of the options are suitable, you may select 'None of the above'."
            
            # system_prompt가 없으면 새로 생성
            if system_prompt:
                system_prompt += f"\n\n{choices_instruction}"
            else:
                system_prompt = choices_instruction

        if system_prompt:
            # history에는 system prompt는 누적되지 않고, 매 요청 시마다 적용합니다.
            system_message = {"role": "system", "content": system_prompt}
            message_history.insert(0, system_message)

        content_blocks: list[dict] = []

        if use_files:
            # Separate PDF files and image files for different handling
            pdf_files = []
            image_files = []

            if human_message.files:
                for file in human_message.files:
                    import mimetypes
                    from pathlib import Path

                    # Determine file type
                    if isinstance(file, str):
                        file_path = Path(file)
                        mime_type, _ = mimetypes.guess_type(str(file_path))
                    else:
                        mime_type, _ = mimetypes.guess_type(getattr(file, "name", ""))

                    if mime_type == "application/pdf":
                        pdf_files.append(file)
                    elif mime_type and mime_type.startswith("image/"):
                        image_files.append(file)
                    else:
                        # Default to image handling for unknown types
                        image_files.append(file)

            # Handle PDF files using base64 encoding (OpenAI's new base64 PDF support)
            if pdf_files:
                for pdf_file in pdf_files:
                    try:
                        import base64
                        from pathlib import Path

                        # Read and encode PDF file
                        if isinstance(pdf_file, str):
                            file_path = Path(pdf_file)
                            filename = file_path.name
                            with open(pdf_file, "rb") as f:
                                file_content = f.read()
                        else:
                            # Reset file pointer if it's a file object
                            if hasattr(pdf_file, "seek"):
                                pdf_file.seek(0)
                            file_content = pdf_file.read()
                            filename = getattr(pdf_file, "name", "document.pdf")
                            # Extract just the filename if it's a full path
                            if hasattr(filename, "split"):
                                filename = filename.split("/")[-1].split("\\")[-1]

                        # Base64 encode the PDF content with proper data URL format
                        base64_content = base64.b64encode(file_content).decode("utf-8")
                        data_url = f"data:application/pdf;base64,{base64_content}"

                        # Add file reference to content using OpenAI's base64 PDF format
                        content_blocks.append({"type": "file", "file": {"filename": filename, "file_data": data_url}})

                    except Exception as e:
                        logger.error(f"Failed to encode PDF file: {e}")
                        # Fallback: try to process as image (conversion will happen in encode_files)
                        image_files.append(pdf_file)

            # Handle image files using existing logic
            if image_files:
                # https://platform.openai.com/docs/guides/images?api-mode=chat
                #  - up to 20MB per image
                #  - low resolution : 512px x 512px
                #  - high resolution : 768px (short side) x 2000px (long side)
                image_urls = encode_files(
                    image_files,
                    allowed_types=[IOType.IMAGE],  # Only images for this path
                    convert_mode="base64",
                )

                if image_urls:
                    for image_url in image_urls:
                        content_blocks.append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                    # "detail": "auto",  # low, high, auto (default)
                                },
                            }
                        )
        else:
            if human_message.files:
                logger.warning("IOs are ignored because use_files flag is set to False.")

        message_history.append(
            {
                "role": human_message.role,
                "content": [
                    *content_blocks,
                    {"type": "text", "text": human_message.content},
                ],
            }
        )

        request_params = {
            "model": model,
            "messages": message_history,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        # choices가 있으면 response_format 추가
        if "choices" in input_context:
            request_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "choice_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "choice": {"type": "string", "enum": input_context["choices"]},
                            "choice_index": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": len(input_context["choices"]) - 1,
                                "description": "Zero-based index of the selected choice",
                            },
                            "confidence": {
                                "type": "number",
                                "minimum": 0.0,
                                "maximum": 1.0,
                                "description": "Confidence level in the selection",
                            },
                        },
                        "required": ["choice", "choice_index", "confidence"],
                        "additionalProperties": False,
                    },
                },
            }
            # structured output을 위해 낮은 temperature 사용
            request_params["temperature"] = 0.1

        # schema가 있으면 response_format 추가 (OpenAI Structured Output 사용)
        elif "schema" in input_context:
            schema = input_context["schema"]
            # schema에 시스템 프롬프트 추가
            if system_prompt:
                system_prompt += (
                    f"\n\nYou must return a JSON response that conforms to this schema: {input_context['schema_json']}"
                )

            request_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "strict": True,
                    "schema": input_context["schema_json"],
                },
            }
            # structured output을 위해 낮은 temperature 사용
            request_params["temperature"] = 0.1

        return request_params

    def _make_ask(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: OpenAIChatModelType,
    ) -> Reply:
        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = self._make_request_params(
            input_context=input_context,
            human_message=human_message,
            messages=messages,
            model=model,
        )

        response: Optional[self._ChatCompletion] = None
        is_cached = False
        cache_key = None

        # Check cache if enabled
        if self.cache:
            from pyhub.llm.cache.utils import generate_cache_key

            cache_key = generate_cache_key("openai", **request_params)
            cached_value = self.cache.get(cache_key)

            if cached_value is not None:
                try:
                    response = self._ChatCompletion.model_validate_json(cached_value)
                    is_cached = True
                except pydantic.ValidationError as e:
                    logger.error("Invalid cached value : %s", e)

        if response is None:
            logger.debug("request to openai")
            response: self._ChatCompletion = sync_client.chat.completions.create(**request_params)

            # Store in cache if enabled
            if self.cache and cache_key:
                self.cache.set(cache_key, response.model_dump_json())

        assert response is not None

        # 캐시된 응답인 경우 usage를 0으로 설정
        usage_input = 0 if is_cached else (response.usage.prompt_tokens or 0)
        usage_output = 0 if is_cached else (response.usage.completion_tokens or 0)

        return Reply(
            text=response.choices[0].message.content,
            usage=Usage(input=usage_input, output=usage_output),
        )

    async def _make_ask_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: OpenAIChatModelType,
    ) -> Reply:
        async_client = self._AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = self._make_request_params(
            input_context=input_context,
            human_message=human_message,
            messages=messages,
            model=model,
        )

        response: Optional[self._ChatCompletion] = None
        is_cached = False
        cache_key = None

        # Check cache if enabled
        if self.cache:
            from pyhub.llm.cache.utils import generate_cache_key

            cache_key = generate_cache_key("openai", **request_params)
            cached_value = self.cache.get(cache_key)

            if cached_value is not None:
                try:
                    response = self._ChatCompletion.model_validate_json(cached_value)
                    is_cached = True
                except pydantic.ValidationError as e:
                    logger.error("Invalid cached value : %s", e)

        if response is None:
            logger.debug("request to openai")
            response = await async_client.chat.completions.create(**request_params)

            # Store in cache if enabled
            if self.cache and cache_key:
                self.cache.set(cache_key, response.model_dump_json())

        assert response is not None

        # 캐시된 응답인 경우 usage를 0으로 설정
        usage_input = 0 if is_cached else (response.usage.prompt_tokens or 0)
        usage_output = 0 if is_cached else (response.usage.completion_tokens or 0)

        return Reply(
            text=response.choices[0].message.content,
            usage=Usage(input=usage_input, output=usage_output),
        )

    def _make_ask_stream(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: OpenAIChatModelType,
    ) -> Generator[Reply, None, None]:
        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = self._make_request_params(
            input_context=input_context,
            human_message=human_message,
            messages=messages,
            model=model,
        )
        request_params["stream"] = True

        # Streaming responses are not cached for now
        if self.cache:
            # TODO: Implement streaming cache support
            pass

        # Add stream_options after cache key generation (if supported)
        if self.supports_stream_options:
            request_params["stream_options"] = {"include_usage": True}

        logger.debug(
            "Request to %s (supports_stream_options=%s, stream_options=%s)",
            self.__class__.__name__,
            self.supports_stream_options,
            request_params.get("stream_options"),
        )

        response_stream = sync_client.chat.completions.create(**request_params)
        usage = None

        reply_list: list[Reply] = []
        chunk_count = 0
        for chunk in response_stream:
            chunk_count += 1
            if chunk.choices and chunk.choices[0].delta.content:  # noqa
                reply = Reply(text=chunk.choices[0].delta.content)
                reply_list.append(reply)
                yield reply
            if chunk.usage:
                logger.debug(
                    "Found usage in sync stream: input=%s, output=%s",
                    chunk.usage.prompt_tokens,
                    chunk.usage.completion_tokens,
                )
                usage = Usage(
                    input=chunk.usage.prompt_tokens or 0,
                    output=chunk.usage.completion_tokens or 0,
                )

        logger.debug("Processed %d chunks from OpenAI stream", chunk_count)
        if usage:
            logger.debug("Yielding final usage chunk with usage info: input=%d, output=%d", usage.input, usage.output)
            reply = Reply(text="", usage=usage)
            reply_list.append(reply)
            yield reply
        else:
            if self.supports_stream_options:
                logger.warning(
                    "No usage information received from %s stream despite stream_options", self.__class__.__name__
                )
            else:
                logger.debug(
                    "No usage information received from %s stream (stream_options not supported)",
                    self.__class__.__name__,
                )

        # Streaming cache not implemented yet

    async def _make_ask_stream_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: OpenAIChatModelType,
    ) -> AsyncGenerator[Reply, None]:
        async_client = self._AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = self._make_request_params(
            input_context=input_context,
            human_message=human_message,
            messages=messages,
            model=model,
        )
        request_params["stream"] = True

        # Streaming responses are not cached for now
        if self.cache:
            # TODO: Implement streaming cache support
            pass

        # Add stream_options after cache key generation (if supported)
        if self.supports_stream_options:
            request_params["stream_options"] = {"include_usage": True}

        logger.debug("request to openai")

        response_stream = await async_client.chat.completions.create(**request_params)
        usage = None

        reply_list: list[Reply] = []
        async for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:  # noqa
                reply = Reply(text=chunk.choices[0].delta.content)
                reply_list.append(reply)
                yield reply
            if chunk.usage:
                usage = Usage(
                    input=chunk.usage.prompt_tokens or 0,
                    output=chunk.usage.completion_tokens or 0,
                )

        if usage:
            logger.debug("Yielding final usage chunk with usage info: input=%d, output=%d", usage.input, usage.output)
            reply = Reply(text="", usage=usage)
            reply_list.append(reply)
            yield reply
        else:
            if self.supports_stream_options:
                logger.warning(
                    "No usage information received from %s stream despite stream_options", self.__class__.__name__
                )
            else:
                logger.debug(
                    "No usage information received from %s stream (stream_options not supported)",
                    self.__class__.__name__,
                )

        # Streaming cache not implemented yet

    def _convert_tools_for_provider(self, tools):
        """OpenAI Function Calling 형식으로 도구 변환"""
        from .tools import ProviderToolConverter

        return [ProviderToolConverter.to_openai_function(tool) for tool in tools]

    def _extract_tool_calls_from_response(self, response):
        """OpenAI 응답에서 tool_calls 추출"""
        tool_calls = []

        # Response가 Reply 객체인 경우 원본 응답에서 tool_calls 추출
        if hasattr(response, "_raw_response") and hasattr(response._raw_response, "choices"):
            message = response._raw_response.choices[0].message
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tool_call in message.tool_calls:
                    try:
                        import json

                        arguments = json.loads(tool_call.function.arguments)
                        tool_calls.append({"id": tool_call.id, "name": tool_call.function.name, "arguments": arguments})
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {tool_call.function.arguments}")

        return tool_calls

    def _make_ask_with_tools_sync(self, human_prompt, messages, tools, tool_choice, model, files):
        """OpenAI Function Calling을 사용한 동기 호출"""
        from .types import Message

        # 메시지 준비
        if human_prompt:
            messages = messages + [Message(role="user", content=human_prompt, files=files)]

        # OpenAI 메시지 형식으로 변환
        openai_messages = []
        for msg in messages:
            openai_msg = {"role": msg.role, "content": msg.content}
            if hasattr(msg, "files") and msg.files:
                # 파일이 있는 경우 처리 (multimodal)
                content = [{"type": "text", "text": msg.content}]
                for file in msg.files:
                    # 이미지 파일 처리 로직 (기존 코드 참조)
                    pass
                openai_msg["content"] = content
            openai_messages.append(openai_msg)

        # OpenAI API 호출
        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = {
            "model": model or self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            request_params["tools"] = tools
            if tool_choice != "auto":
                request_params["tool_choice"] = tool_choice

        try:
            # 디버깅 정보 로깅
            logger.debug(f"Making Function Calling request to {self.base_url}")
            logger.debug(f"Model: {request_params['model']}")
            logger.debug(f"Tools count: {len(tools) if tools else 0}")

            # API 요청 내역 상세 출력
            import json

            logger.debug("=== Function Calling API Request ===")
            logger.debug(f"Endpoint: {self.base_url}/chat/completions")
            logger.debug(f"Headers: Authorization: Bearer {self.api_key[:8]}...")
            logger.debug("Request payload:")
            # 요청 페이로드를 JSON 형태로 예쁘게 출력
            debug_payload = request_params.copy()
            if "messages" in debug_payload and len(debug_payload["messages"]) > 2:
                # 메시지가 너무 길면 요약
                debug_payload["messages"] = debug_payload["messages"][:2] + [
                    {"...": f"({len(debug_payload['messages'])-2} more messages)"}
                ]
            logger.debug(json.dumps(debug_payload, indent=2, ensure_ascii=False))
            logger.debug("=" * 40)

            # Trace 모드에서 콘솔에도 출력
            if llm_settings.trace_function_calls:
                print(f"   🌐 API 요청: {self.base_url}/chat/completions")
                print(f"   📋 모델: {request_params['model']}")
                print(f"   🔧 도구 개수: {len(tools) if tools else 0}")
                if tools:
                    print(f"   🛠️ 도구 목록: {[t['function']['name'] for t in tools]}")
                print(f"   💬 메시지 개수: {len(request_params['messages'])}")

            response = sync_client.chat.completions.create(**request_params)

            # API 응답 디버깅 출력
            logger.debug("=== Function Calling API Response ===")
            logger.debug("Response status: Success")
            logger.debug(f"Usage: input={response.usage.prompt_tokens}, output={response.usage.completion_tokens}")
            logger.debug(
                f"Response content: {response.choices[0].message.content[:200] if response.choices[0].message.content else 'None'}..."
            )
            logger.debug(f"Response finish_reason: {response.choices[0].finish_reason}")
            if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                logger.debug(f"Tool calls: {len(response.choices[0].message.tool_calls)} calls")
                for i, tool_call in enumerate(response.choices[0].message.tool_calls):
                    logger.debug(f"  Tool {i+1}: {tool_call.function.name}({tool_call.function.arguments})")
            else:
                logger.debug("Tool calls: None")
            logger.debug("=" * 40)

            # Trace 모드에서 콘솔에도 응답 출력
            if llm_settings.trace_function_calls:
                print("   ✅ API 응답 성공")
                print(
                    f"   📊 토큰 사용량: 입력={response.usage.prompt_tokens}, 출력={response.usage.completion_tokens}"
                )
                if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                    print(f"   🔧 도구 호출 요청: {len(response.choices[0].message.tool_calls)}개")
                else:
                    print(
                        f"   💬 응답 내용: {response.choices[0].message.content[:100]}...'"
                        if response.choices[0].message.content
                        else "   💬 응답 내용: (없음)"
                    )

            # Reply 객체로 변환
            usage = Usage(input=response.usage.prompt_tokens or 0, output=response.usage.completion_tokens or 0)

            reply = Reply(text=response.choices[0].message.content or "", usage=usage)

            # 원본 응답을 저장하여 tool_calls 추출에 사용
            reply._raw_response = response

            return reply

        except Exception as e:
            # 디버깅 모드에서 에러 상세 출력
            logger.error("=== Async Function Calling API Error ===")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            if hasattr(e, "response"):
                logger.error(f"HTTP status: {getattr(e.response, 'status_code', 'Unknown')}")
                response_text = getattr(e.response, "text", "")
                if response_text:
                    logger.error(f"Response body: {response_text[:1000]}")
            logger.error("=" * 40)

            # Trace 모드에서 콘솔에도 에러 출력
            if llm_settings.trace_function_calls:
                print(f"   ❌ 비동기 API 오류: {type(e).__name__}")
                if hasattr(e, "response") and hasattr(e.response, "status_code"):
                    print(f"   📄 HTTP 상태: {e.response.status_code}")
                    if hasattr(e.response, "text"):
                        print(f"   📝 응답 내용: {e.response.text[:200]}...")

            # HTTP 응답 코드와 상세 정보도 포함
            error_details = str(e)
            if hasattr(e, "response") and hasattr(e.response, "status_code"):
                error_details = f"HTTP {e.response.status_code}: {error_details}"
            if hasattr(e, "response") and hasattr(e.response, "text"):
                error_details += f"\nResponse: {e.response.text[:500]}"
            return Reply(text=f"API Error: {error_details}")

    async def _make_ask_with_tools_async(self, human_prompt, messages, tools, tool_choice, model, files):
        """OpenAI Function Calling을 사용한 비동기 호출"""
        from .types import Message

        # 메시지 준비
        if human_prompt:
            messages = messages + [Message(role="user", content=human_prompt, files=files)]

        # OpenAI 메시지 형식으로 변환
        openai_messages = []
        for msg in messages:
            openai_msg = {"role": msg.role, "content": msg.content}
            if hasattr(msg, "files") and msg.files:
                # 파일이 있는 경우 처리 (multimodal)
                content = [{"type": "text", "text": msg.content}]
                for file in msg.files:
                    # 이미지 파일 처리 로직 (기존 코드 참조)
                    pass
                openai_msg["content"] = content
            openai_messages.append(openai_msg)

        # OpenAI API 호출
        async_client = self._AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = {
            "model": model or self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            request_params["tools"] = tools
            if tool_choice != "auto":
                request_params["tool_choice"] = tool_choice

        try:
            # 디버깅 정보 로깅 (비동기 버전)
            logger.debug(f"Making async Function Calling request to {self.base_url}")
            logger.debug(f"Model: {request_params['model']}")
            logger.debug(f"Tools count: {len(request_params.get('tools', [])) if 'tools' in request_params else 0}")

            # API 요청 내역 상세 출력
            import json

            logger.debug("=== Async Function Calling API Request ===")
            logger.debug(f"Endpoint: {self.base_url}/chat/completions")
            logger.debug(f"Headers: Authorization: Bearer {self.api_key[:8]}...")
            logger.debug("Request payload:")
            debug_payload = request_params.copy()
            if "messages" in debug_payload and len(debug_payload["messages"]) > 2:
                debug_payload["messages"] = debug_payload["messages"][:2] + [
                    {"...": f"({len(debug_payload['messages'])-2} more messages)"}
                ]
            logger.debug(json.dumps(debug_payload, indent=2, ensure_ascii=False))
            logger.debug("=" * 40)

            # Trace 모드에서 콘솔에도 출력
            if llm_settings.trace_function_calls:
                print(f"   🌐 비동기 API 요청: {self.base_url}/chat/completions")
                print(f"   📋 모델: {request_params['model']}")
                print(f"   🔧 도구 개수: {len(tools) if tools else 0}")
                if tools:
                    print(f"   🛠️ 도구 목록: {[t['function']['name'] for t in tools]}")
                print(f"   💬 메시지 개수: {len(request_params['messages'])}")

            response = await async_client.chat.completions.create(**request_params)

            # API 응답 디버깅 출력 (비동기 버전)
            logger.debug("=== Async Function Calling API Response ===")
            logger.debug("Response status: Success")
            logger.debug(f"Usage: input={response.usage.prompt_tokens}, output={response.usage.completion_tokens}")
            logger.debug(
                f"Response content: {response.choices[0].message.content[:200] if response.choices[0].message.content else 'None'}..."
            )
            logger.debug(f"Response finish_reason: {response.choices[0].finish_reason}")
            if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                logger.debug(f"Tool calls: {len(response.choices[0].message.tool_calls)} calls")
                for i, tool_call in enumerate(response.choices[0].message.tool_calls):
                    logger.debug(f"  Tool {i+1}: {tool_call.function.name}({tool_call.function.arguments})")
            else:
                logger.debug("Tool calls: None")
            logger.debug("=" * 40)

            # Trace 모드에서 콘솔에도 응답 출력
            if llm_settings.trace_function_calls:
                print("   ✅ 비동기 API 응답 성공")
                print(
                    f"   📊 토큰 사용량: 입력={response.usage.prompt_tokens}, 출력={response.usage.completion_tokens}"
                )
                if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                    print(f"   🔧 도구 호출 요청: {len(response.choices[0].message.tool_calls)}개")
                else:
                    print(
                        f"   💬 응답 내용: {response.choices[0].message.content[:100]}..."
                        if response.choices[0].message.content
                        else "   💬 응답 내용: (없음)"
                    )

            # Reply 객체로 변환
            usage = Usage(input=response.usage.prompt_tokens or 0, output=response.usage.completion_tokens or 0)

            reply = Reply(text=response.choices[0].message.content or "", usage=usage)

            # 원본 응답을 저장하여 tool_calls 추출에 사용
            reply._raw_response = response

            return reply

        except Exception as e:
            # 디버깅 모드에서 에러 상세 출력
            logger.error("=== Async Function Calling API Error ===")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            if hasattr(e, "response"):
                logger.error(f"HTTP status: {getattr(e.response, 'status_code', 'Unknown')}")
                response_text = getattr(e.response, "text", "")
                if response_text:
                    logger.error(f"Response body: {response_text[:1000]}")
            logger.error("=" * 40)

            # Trace 모드에서 콘솔에도 에러 출력
            if llm_settings.trace_function_calls:
                print(f"   ❌ 비동기 API 오류: {type(e).__name__}")
                if hasattr(e, "response") and hasattr(e.response, "status_code"):
                    print(f"   📄 HTTP 상태: {e.response.status_code}")
                    if hasattr(e.response, "text"):
                        print(f"   📝 응답 내용: {e.response.text[:200]}...")

            # HTTP 응답 코드와 상세 정보도 포함
            error_details = str(e)
            if hasattr(e, "response") and hasattr(e.response, "status_code"):
                error_details = f"HTTP {e.response.status_code}: {error_details}"
            if hasattr(e, "response") and hasattr(e.response, "text"):
                error_details += f"\nResponse: {e.response.text[:500]}"
            return Reply(text=f"API Error: {error_details}")

    def ask(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[OpenAIChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        schema: Optional[Type[BaseModel]] = None,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
    ) -> Union[Reply, Generator[Reply, None, None]]:
        return super().ask(
            input=input,
            files=files,
            model=model,
            context=context,
            choices=choices,
            choices_optional=choices_optional,
            schema=schema,
            stream=stream,
            use_history=use_history,
            raise_errors=raise_errors,
            tools=tools,
            tool_choice=tool_choice,
            max_tool_calls=max_tool_calls,
        )

    async def ask_async(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[OpenAIChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        schema: Optional[Type[BaseModel]] = None,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
    ) -> Union[Reply, AsyncGenerator[Reply, None]]:
        return await super().ask_async(
            input=input,
            files=files,
            model=model,
            context=context,
            choices=choices,
            choices_optional=choices_optional,
            schema=schema,
            stream=stream,
            use_history=use_history,
            raise_errors=raise_errors,
            tools=tools,
            tool_choice=tool_choice,
            max_tool_calls=max_tool_calls,
        )

    def embed(
        self, input: Union[str, list[str]], model: Optional[OpenAIEmbeddingModelType] = None
    ) -> Union[Embed, EmbedList]:
        embedding_model = cast(OpenAIEmbeddingModelType, model or self.embedding_model)

        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = dict(input=input, model=str(embedding_model))

        response: Optional[self._CreateEmbeddingResponse] = None
        is_cached = False
        cache_key = None

        # Check cache if enabled
        if self.cache:
            from pyhub.llm.cache.utils import generate_cache_key

            cache_key = generate_cache_key("openai", **request_params)
            cached_value = self.cache.get(cache_key)

            if cached_value is not None:
                try:
                    response = self._CreateEmbeddingResponse.model_validate_json(cached_value)
                    is_cached = True
                except pydantic.ValidationError as e:
                    logger.error("Invalid cached value : %s", e)

        if response is None:
            logger.debug("request to openai")
            response = sync_client.embeddings.create(**request_params)

            # Store in cache if enabled
            if self.cache and cache_key:
                self.cache.set(cache_key, response.model_dump_json())

        assert response is not None

        # 캐시된 응답인 경우 usage를 0으로 설정
        usage_input = 0 if is_cached else (response.usage.prompt_tokens or 0)
        usage = Usage(input=usage_input, output=0)

        if isinstance(input, str):
            return Embed(response.data[0].embedding, usage=usage)
        return EmbedList([Embed(v.embedding) for v in response.data], usage=usage)

    async def embed_async(
        self, input: Union[str, list[str]], model: Optional[OpenAIEmbeddingModelType] = None
    ) -> Union[Embed, EmbedList]:
        embedding_model = cast(OpenAIEmbeddingModelType, model or self.embedding_model)

        async_client = self._AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        request_params = dict(input=input, model=str(embedding_model))

        response: Optional[self._CreateEmbeddingResponse] = None
        is_cached = False
        cache_key = None

        # Check cache if enabled
        if self.cache:
            from pyhub.llm.cache.utils import generate_cache_key

            cache_key = generate_cache_key("openai", **request_params)
            cached_value = self.cache.get(cache_key)

            if cached_value is not None:
                try:
                    response = self._CreateEmbeddingResponse.model_validate_json(cached_value)
                    is_cached = True
                except pydantic.ValidationError as e:
                    logger.error("Invalid cached value : %s", e)

        if response is None:
            logger.debug("request to openai")
            response = await async_client.embeddings.create(**request_params)

            # Store in cache if enabled
            if self.cache and cache_key:
                self.cache.set(cache_key, response.model_dump_json())

        assert response is not None

        # 캐시된 응답인 경우 usage를 0으로 설정
        usage_input = 0 if is_cached else (response.usage.prompt_tokens or 0)
        usage = Usage(input=usage_input, output=0)

        if isinstance(input, str):
            return Embed(response.data[0].embedding, usage=usage)
        return EmbedList([Embed(v.embedding) for v in response.data], usage=usage)
    
    def generate_image(
        self,
        prompt: str,
        *,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: Optional[str] = None,
        n: int = 1,
        response_format: str = "url",
        **kwargs
    ) -> ImageReply:
        """Generate images using DALL-E models."""
        from pyhub.llm.constants import (
            IMAGE_GENERATION_DEFAULTS,
            IMAGE_GENERATION_SIZES,
            IMAGE_GENERATION_QUALITIES,
            IMAGE_GENERATION_STYLES,
        )
        
        # Check if current model supports image generation
        if not self.model.startswith(("dall-e-")):
            raise ValueError(
                f"Model '{self.model}' does not support image generation. "
                f"Use 'dall-e-3' or 'dall-e-2' instead."
            )
        
        # Get defaults for the model
        model_defaults = IMAGE_GENERATION_DEFAULTS.get(self.model, {})
        size = size or model_defaults.get("size", "1024x1024")
        quality = quality or model_defaults.get("quality", "standard")
        style = style or model_defaults.get("style")
        
        # Validate size
        valid_sizes = IMAGE_GENERATION_SIZES.get(self.model, [])
        if valid_sizes and size not in valid_sizes:
            raise ValueError(
                f"Invalid size '{size}' for model '{self.model}'. "
                f"Valid sizes are: {', '.join(valid_sizes)}"
            )
        
        # Validate quality
        valid_qualities = IMAGE_GENERATION_QUALITIES.get(self.model, [])
        if valid_qualities and quality not in valid_qualities:
            raise ValueError(
                f"Invalid quality '{quality}' for model '{self.model}'. "
                f"Valid qualities are: {', '.join(valid_qualities)}"
            )
        
        # Validate style (only for models that support it)
        valid_styles = IMAGE_GENERATION_STYLES.get(self.model, [])
        if style and valid_styles and style not in valid_styles:
            raise ValueError(
                f"Invalid style '{style}' for model '{self.model}'. "
                f"Valid styles are: {', '.join(valid_styles)}"
            )
        
        # Create client
        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        
        # Build request parameters
        request_params = {
            "model": self.model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n,
            "response_format": response_format,
        }
        
        # Add style only if supported and provided
        if style and valid_styles:
            request_params["style"] = style
        
        # Make API call
        response = sync_client.images.generate(**request_params)
        
        # Extract first image data
        image_data = response.data[0]
        
        # Build ImageReply
        return ImageReply(
            url=image_data.url if response_format == "url" else None,
            base64_data=image_data.b64_json if response_format == "b64_json" else None,
            revised_prompt=getattr(image_data, "revised_prompt", None),
            size=size,
            model=self.model,
            usage=None  # OpenAI image generation doesn't provide usage info
        )
    
    def supports(self, capability: str) -> bool:
        """Check if the current model supports a specific capability."""
        if capability == "image_generation":
            return self.model.startswith(("dall-e-"))
        return super().supports(capability)
    
    def get_supported_image_sizes(self) -> list[str]:
        """Get the list of supported image sizes for the current model."""
        from pyhub.llm.constants import IMAGE_GENERATION_SIZES
        
        if self.model.startswith(("dall-e-")):
            return IMAGE_GENERATION_SIZES.get(self.model, [])
        return []
    
    @property
    def capabilities(self) -> dict[str, Any]:
        """Get the capabilities of the current model."""
        from pyhub.llm.constants import (
            IMAGE_GENERATION_SIZES,
            IMAGE_GENERATION_QUALITIES,
            IMAGE_GENERATION_STYLES,
        )
        
        caps = {}
        
        # Image generation capabilities
        if self.model.startswith(("dall-e-")):
            caps["image_generation"] = {
                "supported": True,
                "sizes": IMAGE_GENERATION_SIZES.get(self.model, []),
                "qualities": IMAGE_GENERATION_QUALITIES.get(self.model, []),
                "styles": IMAGE_GENERATION_STYLES.get(self.model, []),
            }
        else:
            caps["image_generation"] = {"supported": False}
        
        return caps
    
    async def generate_image_async(
        self,
        prompt: str,
        *,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: Optional[str] = None,
        n: int = 1,
        response_format: str = "url",
        **kwargs
    ) -> ImageReply:
        """Asynchronously generate images using DALL-E models."""
        from pyhub.llm.constants import (
            IMAGE_GENERATION_DEFAULTS,
            IMAGE_GENERATION_SIZES,
            IMAGE_GENERATION_QUALITIES,
            IMAGE_GENERATION_STYLES,
        )
        
        # Check if current model supports image generation
        if not self.model.startswith(("dall-e-")):
            raise ValueError(
                f"Model '{self.model}' does not support image generation. "
                f"Use 'dall-e-3' or 'dall-e-2' instead."
            )
        
        # Get defaults for the model
        model_defaults = IMAGE_GENERATION_DEFAULTS.get(self.model, {})
        size = size or model_defaults.get("size", "1024x1024")
        quality = quality or model_defaults.get("quality", "standard")
        style = style or model_defaults.get("style")
        
        # Validate size
        valid_sizes = IMAGE_GENERATION_SIZES.get(self.model, [])
        if valid_sizes and size not in valid_sizes:
            raise ValueError(
                f"Invalid size '{size}' for model '{self.model}'. "
                f"Valid sizes are: {', '.join(valid_sizes)}"
            )
        
        # Validate quality
        valid_qualities = IMAGE_GENERATION_QUALITIES.get(self.model, [])
        if valid_qualities and quality not in valid_qualities:
            raise ValueError(
                f"Invalid quality '{quality}' for model '{self.model}'. "
                f"Valid qualities are: {', '.join(valid_qualities)}"
            )
        
        # Validate style (only for models that support it)
        valid_styles = IMAGE_GENERATION_STYLES.get(self.model, [])
        if style and valid_styles and style not in valid_styles:
            raise ValueError(
                f"Invalid style '{style}' for model '{self.model}'. "
                f"Valid styles are: {', '.join(valid_styles)}"
            )
        
        # Create async client
        async_client = self._AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        
        # Build request parameters
        request_params = {
            "model": self.model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n,
            "response_format": response_format,
        }
        
        # Add style only if supported and provided
        if style and valid_styles:
            request_params["style"] = style
        
        # Make API call
        response = await async_client.images.generate(**request_params)
        
        # Extract first image data
        image_data = response.data[0]
        
        # Build ImageReply
        return ImageReply(
            url=image_data.url if response_format == "url" else None,
            base64_data=image_data.b64_json if response_format == "b64_json" else None,
            revised_prompt=getattr(image_data, "revised_prompt", None),
            size=size,
            model=self.model,
            usage=None  # OpenAI image generation doesn't provide usage info
        )


class OpenAILLM(OpenAIMixin, BaseLLM):
    SUPPORTED_FILE_TYPES = [IOType.IMAGE, IOType.PDF]  # OpenAI는 PDF 직접 지원
    EMBEDDING_DIMENSIONS = {
        "text-embedding-ada-002": 1536,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "embedding-query": 4096,
        "embedding-passage": 4096,
    }

    def __init__(
        self,
        model: OpenAIChatModelType = "gpt-4o-mini",
        embedding_model: OpenAIEmbeddingModelType = "text-embedding-3-small",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        system_prompt: Optional[Union[str, Template]] = None,
        prompt: Optional[Union[str, Template]] = None,
        output_key: str = "text",
        initial_messages: Optional[list[Message]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tools: Optional[list] = None,
        **kwargs,
    ):
        # Lazy import openai
        try:
            import openai
            from openai import AsyncOpenAI
            from openai import OpenAI as SyncOpenAI
            from openai.types import CreateEmbeddingResponse
            from openai.types.chat import ChatCompletion

            self._openai = openai
            self._AsyncOpenAI = AsyncOpenAI
            self._SyncOpenAI = SyncOpenAI
            self._CreateEmbeddingResponse = CreateEmbeddingResponse
            self._ChatCompletion = ChatCompletion
        except ImportError:
            raise ImportError("openai package not installed. " "Install with: pip install pyhub-llm[openai]")

        super().__init__(
            model=model,
            embedding_model=embedding_model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            prompt=prompt,
            output_key=output_key,
            initial_messages=initial_messages,
            api_key=api_key or llm_settings.openai_api_key,
            tools=tools,
            **kwargs,
        )
        self.base_url = base_url or llm_settings.openai_base_url

    def check(self) -> list[dict]:
        errors = super().check()

        if not self.api_key or not self.api_key.startswith("sk-"):
            errors.append(
                {
                    "msg": "OpenAI API key is not set or is invalid.",
                    "hint": "Please check your OpenAI API key.",
                    "obj": self,
                }
            )

        return errors
