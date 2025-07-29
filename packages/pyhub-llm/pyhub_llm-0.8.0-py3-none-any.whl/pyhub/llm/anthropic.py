import logging
import re
from pathlib import Path
from typing import IO, Any, AsyncGenerator, Generator, Optional, Union

import pydantic

from pyhub.llm.base import BaseLLM
from pyhub.llm.settings import llm_settings
from pyhub.llm.types import (
    AnthropicChatModelType,
    Embed,
    EmbedList,
    Message,
    Reply,
    Usage,
)
from pyhub.llm.utils.files import IOType, encode_files
from pyhub.llm.utils.templates import Template

logger = logging.getLogger(__name__)


class AnthropicLLM(BaseLLM):
    SUPPORTED_FILE_TYPES = [IOType.IMAGE, IOType.PDF]  # Anthropic도 PDF 직접 지원 (베타)

    def __init__(
        self,
        model: AnthropicChatModelType = "claude-3-5-haiku-latest",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        system_prompt: Optional[Union[str, Template]] = None,
        prompt: Optional[Union[str, Template]] = None,
        output_key: str = "text",
        initial_messages: Optional[list[Message]] = None,
        api_key: Optional[str] = None,
        tools: Optional[list] = None,
        **kwargs,
    ):
        # Lazy import anthropic
        try:
            import anthropic
            import anthropic.types
            from anthropic import NOT_GIVEN as ANTHROPIC_NOT_GIVEN
            from anthropic import Anthropic as SyncAnthropic
            from anthropic import AsyncAnthropic

            self._anthropic = anthropic
            self._anthropic_types = anthropic.types
            self._ANTHROPIC_NOT_GIVEN = ANTHROPIC_NOT_GIVEN
            self._SyncAnthropic = SyncAnthropic
            self._AsyncAnthropic = AsyncAnthropic
        except ImportError:
            raise ImportError("anthropic package not installed. " "Install with: pip install pyhub-llm[anthropic]")

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            prompt=prompt,
            output_key=output_key,
            initial_messages=initial_messages,
            api_key=api_key or llm_settings.anthropic_api_key,
            tools=tools,
            **kwargs,
        )

    def check(self) -> list[dict]:
        errors = super().check()

        if not self.api_key or not self.api_key.startswith("sk-ant-"):
            errors.append(
                {
                    "msg": "Anthropic API key is not set or is invalid.",
                    "hint": "Please check your Anthropic API key.",
                    "obj": self,
                }
            )

        return errors

    def _make_request_params(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: AnthropicChatModelType,
    ) -> dict:
        message_history = [dict(message) for message in messages]

        # choices가 있으면 시스템 프롬프트 수정
        system_prompt = self.get_system_prompt(input_context, default=self._ANTHROPIC_NOT_GIVEN)
        if "choices" in input_context:
            choices_instruction = f"\n\nYou MUST select exactly one option from: {', '.join(input_context['choices'])}."
            if input_context.get("allow_none"):
                choices_instruction += " If none are suitable, select 'None of the above'."
            choices_instruction += "\nRespond with ONLY the chosen option text, nothing else."

            if system_prompt == self._ANTHROPIC_NOT_GIVEN:
                system_prompt = choices_instruction
            else:
                system_prompt += choices_instruction

        # schema가 있으면 JSON 응답을 요청하는 지시사항 추가
        elif "schema" in input_context:
            import json

            schema_json = input_context["schema_json"]
            schema_instruction = (
                f"\n\nYou MUST respond with a valid JSON object that conforms to this schema:\n"
                f"```json\n{json.dumps(schema_json, indent=2)}\n```\n"
                f"Do not include any text before or after the JSON object."
            )
            if system_prompt == self._ANTHROPIC_NOT_GIVEN:
                system_prompt = schema_instruction.strip()
            else:
                system_prompt += schema_instruction

        # https://docs.anthropic.com/en/docs/build-with-claude/vision
        # https://docs.anthropic.com/en/docs/build-with-claude/pdf-support
        image_urls = encode_files(
            human_message.files,
            allowed_types=self.SUPPORTED_FILE_TYPES,
            convert_mode="base64",
        )

        image_blocks: list[dict] = []
        if image_urls:
            base64_url_pattern = r"^data:([^;]+);base64,(.+)"

            for image_url in image_urls:
                base64_url_match = re.match(base64_url_pattern, image_url)
                if base64_url_match:
                    mimetype = base64_url_match.group(1)
                    b64_str = base64_url_match.group(2)
                    image_blocks.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mimetype,
                                "data": b64_str,
                            },
                        }
                    )
                else:
                    image_blocks.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": image_url,
                            },
                        }
                    )

        message_history.append(
            {
                "role": human_message.role,
                "content": [
                    *image_blocks,
                    {"type": "text", "text": human_message.content},
                ],
            }
        )

        params = dict(
            model=model,
            messages=message_history,
            temperature=(
                self.temperature if "choices" not in input_context and "schema" not in input_context else 0.1
            ),  # choices나 schema가 있으면 낮은 temperature
            max_tokens=self.max_tokens,
        )

        # system_prompt가 self._ANTHROPIC_NOT_GIVEN이 아닌 경우에만 추가
        if system_prompt != self._ANTHROPIC_NOT_GIVEN:
            params["system"] = system_prompt

        return params

    def _make_ask(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: AnthropicChatModelType,
    ) -> Reply:
        try:
            sync_client = self._SyncAnthropic(api_key=self.api_key)
            request_params = self._make_request_params(
                input_context=input_context, human_message=human_message, messages=messages, model=model
            )

            response: Optional[self._anthropic_types.Message] = None
            is_cached = False
            cache_key = None

            # Check cache if enabled
            if self.cache and input_context.get("enable_cache", False):
                from pyhub.llm.cache.utils import generate_cache_key

                cache_key = generate_cache_key("anthropic", **request_params)
                cached_value = self.cache.get(cache_key)

                if cached_value is not None:
                    try:
                        response = self._anthropic_types.Message.model_validate_json(cached_value)
                        is_cached = True
                    except pydantic.ValidationError as e:
                        logger.error("cached_value is valid : %s", e)

            if response is None:
                logger.debug("request to anthropic")
                response = sync_client.messages.create(**request_params)

                # Store in cache if enabled
                if self.cache and input_context.get("enable_cache", False) and cache_key:
                    self.cache.set(cache_key, response.model_dump_json())

            assert response is not None

            # 캐시된 응답인 경우 usage를 0으로 설정
            usage_input = 0 if is_cached else (response.usage.input_tokens or 0)
            usage_output = 0 if is_cached else (response.usage.output_tokens or 0)

            return Reply(
                text=response.content[0].text,
                usage=Usage(input=usage_input, output=usage_output),
            )
        except Exception as e:
            logger.error(f"Error in _make_ask: {e}")
            return Reply(text=f"Error: {str(e)}", usage=None)

    async def _make_ask_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: AnthropicChatModelType,
    ) -> Reply:
        async_client = self._AsyncAnthropic(api_key=self.api_key)
        request_params = self._make_request_params(
            input_context=input_context, human_message=human_message, messages=messages, model=model
        )

        response: Optional[self._anthropic_types.Message] = None
        is_cached = False
        cache_key = None

        # Check cache if enabled
        if self.cache:
            from pyhub.llm.cache.utils import generate_cache_key

            cache_key = generate_cache_key("anthropic", **request_params)
            cached_value = self.cache.get(cache_key)

            if cached_value is not None:
                try:
                    response = self._anthropic_types.Message.model_validate_json(cached_value)
                    is_cached = True
                except pydantic.ValidationError as e:
                    logger.error("cached_value is valid : %s", e)

        if response is None:
            logger.debug("request to anthropic")
            response = await async_client.messages.create(**request_params)

            # Store in cache if enabled
            if self.cache and cache_key:
                self.cache.set(cache_key, response.model_dump_json())

        assert response is not None

        # 캐시된 응답인 경우 usage를 0으로 설정
        usage_input = 0 if is_cached else (response.usage.input_tokens or 0)
        usage_output = 0 if is_cached else (response.usage.output_tokens or 0)

        return Reply(
            text=response.content[0].text,
            usage=Usage(input=usage_input, output=usage_output),
        )

    def _make_ask_stream(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: AnthropicChatModelType,
    ) -> Generator[Reply, None, None]:

        sync_client = self._SyncAnthropic(api_key=self.api_key)
        request_params = self._make_request_params(
            input_context=input_context, human_message=human_message, messages=messages, model=model
        )
        request_params["stream"] = True

        # Streaming responses are not cached for now
        if self.cache:
            # TODO: Implement streaming cache support
            pass

        logger.debug("request to anthropic")

        response = sync_client.messages.create(**request_params)

        input_tokens = 0
        output_tokens = 0

        reply_list: list[Reply] = []
        for chunk in response:
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                reply = Reply(text=chunk.delta.text)
                reply_list.append(reply)
                yield reply
            elif hasattr(chunk, "type") and chunk.type == "content_block_delta":
                if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                    reply = Reply(text=chunk.delta.text)
                    reply_list.append(reply)
                    yield reply
                elif hasattr(chunk, "content_block") and hasattr(chunk.content_block, "text"):
                    reply = Reply(text=chunk.content_block.text)
                    reply_list.append(reply)
                    yield reply

            if hasattr(chunk, "message") and hasattr(chunk.message, "usage"):
                input_tokens += getattr(chunk.message.usage, "input_tokens", None) or 0
                output_tokens += getattr(chunk.message.usage, "output_tokens", None) or 0

            if hasattr(chunk, "usage") and chunk.usage:
                input_tokens += getattr(chunk.usage, "input_tokens", None) or 0
                output_tokens += getattr(chunk.usage, "output_tokens", None) or 0

        reply = Reply(text="", usage=Usage(input_tokens, output_tokens))
        reply_list.append(reply)
        yield reply

        # Streaming cache not implemented yet

    async def _make_ask_stream_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: AnthropicChatModelType,
    ) -> AsyncGenerator[Reply, None]:

        async_client = self._AsyncAnthropic(api_key=self.api_key)
        request_params = self._make_request_params(
            input_context=input_context, human_message=human_message, messages=messages, model=model
        )
        request_params["stream"] = True

        # Streaming responses are not cached for now
        if self.cache:
            # TODO: Implement streaming cache support
            pass

        logger.debug("request to anthropic")
        response = await async_client.messages.create(**request_params)

        input_tokens = 0
        output_tokens = 0

        reply_list: list[Reply] = []
        async for chunk in response:
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                reply = Reply(text=chunk.delta.text)
                reply_list.append(reply)
                yield reply
            elif hasattr(chunk, "type") and chunk.type == "content_block_delta":
                if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                    reply = Reply(text=chunk.delta.text)
                    reply_list.append(reply)
                    yield reply
                elif hasattr(chunk, "content_block") and hasattr(chunk.content_block, "text"):
                    reply = Reply(text=chunk.content_block.text)
                    reply_list.append(reply)
                    yield reply

            if hasattr(chunk, "message") and hasattr(chunk.message, "usage"):
                input_tokens += getattr(chunk.message.usage, "input_tokens", None) or 0
                output_tokens += getattr(chunk.message.usage, "output_tokens", None) or 0

            if hasattr(chunk, "usage") and chunk.usage:
                input_tokens += getattr(chunk.usage, "input_tokens", None) or 0
                output_tokens += getattr(chunk.usage, "output_tokens", None) or 0

        reply = Reply(text="", usage=Usage(input_tokens, output_tokens))
        reply_list.append(reply)
        yield reply

        # Streaming cache not implemented yet

    def ask(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[AnthropicChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
        schema: Optional[type[pydantic.BaseModel]] = None,
    ) -> Union[Reply, Generator[Reply, None, None]]:
        return super().ask(
            input=input,
            files=files,
            model=model,
            context=context,
            choices=choices,
            choices_optional=choices_optional,
            stream=stream,
            use_history=use_history,
            raise_errors=raise_errors,
            tools=tools,
            tool_choice=tool_choice,
            max_tool_calls=max_tool_calls,
            schema=schema,
        )

    async def ask_async(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[AnthropicChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        stream: bool = False,
        raise_errors: bool = False,
        use_history: bool = True,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
        schema: Optional[type[pydantic.BaseModel]] = None,
    ) -> Union[Reply, AsyncGenerator[Reply, None]]:
        return await super().ask_async(
            input=input,
            files=files,
            model=model,
            context=context,
            choices=choices,
            choices_optional=choices_optional,
            stream=stream,
            use_history=use_history,
            raise_errors=raise_errors,
            tools=tools,
            tool_choice=tool_choice,
            max_tool_calls=max_tool_calls,
            schema=schema,
        )

    def embed(
        self,
        input: Union[str, list[str]],
        model=None,
    ) -> Union[Embed, EmbedList]:
        raise NotImplementedError("Anthropic does not support embeddings")

    async def embed_async(
        self,
        input: Union[str, list[str]],
        model=None,
    ) -> Union[Embed, EmbedList]:
        raise NotImplementedError("Anthropic does not support embeddings")

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
    ) -> "ImageReply":
        """Generate images from text prompts.
        
        Raises:
            NotImplementedError: Anthropic does not support image generation
        """
        raise NotImplementedError(
            "Anthropic does not support image generation. "
            "Please use a provider that supports image generation, such as OpenAI with DALL-E models."
        )

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
    ) -> "ImageReply":
        """Asynchronously generate images from text prompts.
        
        Raises:
            NotImplementedError: Anthropic does not support image generation
        """
        raise NotImplementedError(
            "Anthropic does not support image generation. "
            "Please use a provider that supports image generation, such as OpenAI with DALL-E models."
        )

    def _convert_tools_for_provider(self, tools):
        """Anthropic Tool Use 형식으로 도구 변환"""
        from .tools import ProviderToolConverter

        return [ProviderToolConverter.to_anthropic_tool(tool) for tool in tools]

    def _extract_tool_calls_from_response(self, response):
        """Anthropic 응답에서 tool_use 추출"""
        tool_calls = []

        # Response가 Reply 객체인 경우 원본 응답에서 tool_use 추출
        if hasattr(response, "_raw_response") and hasattr(response._raw_response, "content"):
            for content in response._raw_response.content:
                if content.type == "tool_use":
                    tool_calls.append({"id": content.id, "name": content.name, "arguments": content.input})

        return tool_calls

    def _make_ask_with_tools_sync(self, human_prompt, messages, tools, tool_choice, model, files):
        """Anthropic Tool Use를 사용한 동기 호출"""

        # 메시지 준비
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({"role": msg.role, "content": msg.content})

        if human_prompt:
            anthropic_messages.append({"role": "user", "content": human_prompt})

        # Anthropic API 호출
        sync_client = self._SyncAnthropic(api_key=self.api_key)
        request_params = {
            "model": model or self.model,
            "messages": anthropic_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            request_params["tools"] = tools

        try:
            response = sync_client.messages.create(**request_params)

            # Reply 객체로 변환
            content_text = ""
            for content in response.content:
                if content.type == "text":
                    content_text += content.text

            usage = Usage(input=response.usage.input_tokens or 0, output=response.usage.output_tokens or 0)

            reply = Reply(text=content_text, usage=usage)

            # 원본 응답을 저장하여 tool_use 추출에 사용
            reply._raw_response = response

            return reply

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return Reply(text=f"API Error: {str(e)}")

    async def _make_ask_with_tools_async(self, human_prompt, messages, tools, tool_choice, model, files):
        """Anthropic Tool Use를 사용한 비동기 호출"""

        # 메시지 준비
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({"role": msg.role, "content": msg.content})

        if human_prompt:
            anthropic_messages.append({"role": "user", "content": human_prompt})

        # Anthropic API 호출
        async_client = self._AsyncAnthropic(api_key=self.api_key)
        request_params = {
            "model": model or self.model,
            "messages": anthropic_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            request_params["tools"] = tools

        try:
            response = await async_client.messages.create(**request_params)

            # Reply 객체로 변환
            content_text = ""
            for content in response.content:
                if content.type == "text":
                    content_text += content.text

            usage = Usage(input=response.usage.input_tokens or 0, output=response.usage.output_tokens or 0)

            reply = Reply(text=content_text, usage=usage)

            # 원본 응답을 저장하여 tool_use 추출에 사용
            reply._raw_response = response

            return reply

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return Reply(text=f"API Error: {str(e)}")


__all__ = ["AnthropicLLM"]
