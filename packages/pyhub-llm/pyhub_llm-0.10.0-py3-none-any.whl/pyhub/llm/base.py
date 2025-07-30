import abc
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Callable,
    Generator,
    List,
    Optional,
    Type,
    Union,
    cast,
)

from pyhub.llm.cache.base import BaseCache
from pyhub.llm.settings import llm_settings

if TYPE_CHECKING:
    from pydantic import BaseModel

    from pyhub.llm.history.base import HistoryBackup
    from pyhub.llm.mcp.configs import McpConfig
    from pyhub.llm.mcp.policy import MCPConnectionPolicy

from pyhub.llm.types import (
    ChainReply,
    Embed,
    EmbedList,
    ImageReply,
    LLMChatModelType,
    LLMEmbeddingModelType,
    Message,
    Reply,
)
from pyhub.llm.utils.files import IOType
from pyhub.llm.utils.templates import (
    Context,
    Template,
    TemplateDoesNotExist,
    async_to_sync,
    get_template,
)

if TYPE_CHECKING:
    from pyhub.llm.history.base import HistoryBackup

logger = logging.getLogger(__name__)


class TemplateDict(dict):
    """템플릿 변수 중 존재하지 않는 키는 원래 형태({key})로 유지하는 딕셔너리"""

    def __missing__(self, key):
        return "{" + key + "}"


@dataclass
class DescribeImageRequest:
    image: Union[str, Path, IO]
    image_path: str
    system_prompt: Union[str, Template]
    user_prompt: Union[str, Template]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    prompt_context: Optional[dict[str, Any]] = None


class BaseLLM(abc.ABC):
    EMBEDDING_DIMENSIONS = {}
    SUPPORTED_FILE_TYPES = [IOType.IMAGE]  # 기본값: 이미지만 지원

    def __init__(
        self,
        model: LLMChatModelType = "gpt-4o-mini",
        embedding_model: LLMEmbeddingModelType = "text-embedding-3-small",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        system_prompt: Optional[Union[str, Template]] = None,
        prompt: Optional[Union[str, Template]] = None,
        output_key: str = "text",
        initial_messages: Optional[list[Message]] = None,
        api_key: Optional[str] = None,
        tools: Optional[list] = None,
        cache: Optional[BaseCache] = None,
        mcp_servers: Optional[Union[str, dict, List[Union[dict, "McpConfig"]], "McpConfig"]] = None,
        mcp_policy: Optional["MCPConnectionPolicy"] = None,
        history_backup: Optional["HistoryBackup"] = None,
        stateless: bool = False,
        include_raw_response: bool = False,
        enable_tracing: Optional[bool] = None,
    ):
        self.model = model
        self.embedding_model = embedding_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.prompt = prompt
        self.output_key = output_key
        self.history_backup = history_backup
        self.stateless = stateless
        self.include_raw_response = include_raw_response

        # Tracing configuration
        self.enable_tracing = enable_tracing if enable_tracing is not None else llm_settings.trace_enabled
        self._last_usage = None  # Store last token usage for tracing

        # 백업이 있으면 히스토리 복원, 없으면 initial_messages 사용
        if self.history_backup:
            try:
                self.history = self.history_backup.load_history()
            except Exception as e:
                # 복원 실패 시 initial_messages 사용
                logger.warning(f"Failed to load history from backup: {e}")
                self.history = initial_messages or []
        else:
            self.history = initial_messages or []
        self.api_key = api_key
        self.cache = cache

        # MCP 설정 처리 (파일 경로, dict, list, McpConfig 지원)
        self.mcp_servers = self._process_mcp_servers(mcp_servers)
        self.mcp_policy = mcp_policy
        self._mcp_client = None
        self._mcp_connected = False
        self._mcp_tools = []

        # 기본 도구 설정
        self.default_tools = []
        if tools:
            # tools 모듈을 동적 import (순환 import 방지)
            from .tools import ToolAdapter

            self.default_tools = ToolAdapter.adapt_tools(tools)

        # Finalizer 등록 (MCP 사용 시)
        self._finalizer = None
        if self.mcp_servers:
            from .resource_manager import register_mcp_instance

            self._finalizer = register_mcp_instance(self)

    def _process_mcp_servers(self, mcp_servers) -> List["McpConfig"]:
        """MCP 서버 설정을 처리합니다."""
        if not mcp_servers:
            return []

        # 문자열인 경우 파일 경로로 처리
        if isinstance(mcp_servers, str):
            # 동적 import (순환 import 방지)
            from .mcp import load_mcp_config

            return load_mcp_config(mcp_servers)

        # dict인 경우 (mcpServers 키가 있을 수 있음)
        elif isinstance(mcp_servers, dict):
            from .mcp import load_mcp_config

            return load_mcp_config(mcp_servers)

        # list인 경우
        elif isinstance(mcp_servers, list):
            # 리스트의 각 요소가 dict인지 확인
            if all(isinstance(item, dict) for item in mcp_servers):
                from .mcp import load_mcp_config

                return load_mcp_config(mcp_servers)
            else:
                # McpConfig 인스턴스 리스트인 경우 그대로 반환
                return mcp_servers

        # 단일 McpConfig 인스턴스인 경우
        else:
            return [mcp_servers]

    def check(self) -> list[dict]:
        """Check configuration and return list of error dicts"""
        return []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model}, embedding_model={self.embedding_model}, temperature={self.temperature}, max_tokens={self.max_tokens})"

    def __len__(self) -> int:
        return len(self.history)

    @property
    def is_stateless(self) -> bool:
        """현재 인스턴스가 stateless 모드인지 확인"""
        return self.stateless

    def __or__(self, next_llm: Union["BaseLLM", "SequentialChain"]) -> "SequentialChain":
        if isinstance(next_llm, BaseLLM):
            return SequentialChain(self, next_llm)
        elif isinstance(next_llm, SequentialChain):
            next_llm.insert_first(self)
            return next_llm
        else:
            raise TypeError("next_llm must be an instance of BaseLLM or SequentialChain")

    def __ror__(self, prev_llm: Union["BaseLLM", "SequentialChain"]) -> "SequentialChain":
        if isinstance(prev_llm, BaseLLM):
            return SequentialChain(prev_llm, self)
        elif isinstance(prev_llm, SequentialChain):
            prev_llm.append(self)
            return prev_llm
        else:
            raise TypeError("prev_llm must be an instance of BaseLLM or SequentialChain")

    def clear(self):
        """Clear the chat history"""
        # stateless 모드에서는 이미 history가 비어있으므로 아무 동작 안 함
        if not self.stateless:
            self.history = []

    def _process_template(self, template: Union[str, Template], context: dict[str, Any]) -> Optional[str]:
        """템플릿 처리를 위한 공통 메서드"""
        # Django Template 객체인 경우
        if hasattr(template, "render"):
            logger.debug("using template render : %s", template)
            return template.render(Context(context))

        # 문자열인 경우
        elif isinstance(template, str):
            # 파일 기반 템플릿 처리
            if "prompts/" in template and template.endswith((".txt", ".md", ".yaml")):
                try:
                    template_obj = get_template(template)
                    logger.debug("using template render : %s", template)
                    return template_obj.render(context)
                except TemplateDoesNotExist:
                    logger.debug("Template '%s' does not exist", template)
                    return None
            # 장고 템플릿 문법의 문자열
            elif "{{" in template or "{%" in template:
                logger.debug("using string template render : %s ...", repr(template))
                return Template(template).render(Context(context))
            # 일반 문자열 포맷팅 - 존재하는 키만 치환하고 나머지는 그대로 유지
            if context:
                try:
                    return template.format_map(TemplateDict(context))
                except Exception as e:
                    logger.debug("Template formatting failed: %s", e)
                    return template
            return template

        return None

    def get_system_prompt(self, input_context: dict[str, Any], default: Any = None) -> Optional[str]:
        if not self.system_prompt:
            return default

        return self._process_template(self.system_prompt, input_context)

    def get_human_prompt(self, input: Union[str, dict[str, Any]], context: dict[str, Any]) -> str:
        if isinstance(input, (str, Template)) or hasattr(input, "render"):
            result = self._process_template(input, context)
            if result is not None:
                return result

        elif isinstance(input, dict):
            if self.prompt:
                # prompt가 있으면 템플릿 렌더링
                result = self._process_template(self.prompt, context)
                if result is not None:
                    return result
            else:
                # prompt가 없으면 dict를 자동으로 포맷팅
                # context에서 'user_message' 키가 있으면 그것을 사용
                if "user_message" in context:
                    return str(context["user_message"])
                # 아니면 dict의 내용을 읽기 쉬운 형태로 변환
                formatted_parts = []
                for key, value in context.items():
                    if key not in ["choices", "choices_formatted", "choices_optional"]:
                        formatted_parts.append(f"{key}: {value}")
                return "\n".join(formatted_parts) if formatted_parts else ""

        raise ValueError(f"input must be a str, Template, or dict, but got {type(input)}")

    def _update_history(
        self,
        human_message: Message,
        ai_message: Union[str, Message],
        tool_interactions: Optional[list[dict]] = None,
    ) -> None:
        # stateless 모드에서는 history를 업데이트하지 않음
        if self.stateless:
            return

        if isinstance(ai_message, str):
            ai_message = Message(role="assistant", content=ai_message, tool_interactions=tool_interactions)
        elif tool_interactions and not ai_message.tool_interactions:
            # tool_interactions가 제공되었지만 ai_message에 없는 경우
            ai_message.tool_interactions = tool_interactions

        # 메모리에 저장
        self.history.extend(
            [
                human_message,
                ai_message,
            ]
        )

        # 백업이 있으면 백업 수행
        if self.history_backup:
            try:
                # usage 정보를 위해 _last_usage 속성 확인
                usage = getattr(self, "_last_usage", None)
                self.history_backup.save_exchange(
                    user_msg=human_message, assistant_msg=ai_message, usage=usage, model=self.model
                )
            except Exception as e:
                # 백업 실패해도 계속 진행
                logger.warning(f"History backup failed: {e}")

    def get_output_key(self) -> str:
        return self.output_key

    def _process_choice_response(
        self, text: str, choices: list[str], choices_optional: bool
    ) -> tuple[Optional[str], Optional[int], float]:
        """
        응답 텍스트에서 choice를 추출하고 검증

        Returns:
            (choice, index, confidence) 튜플
        """
        import re

        # JSON 응답 파싱 시도 (OpenAI, Google 등)
        try:
            import json

            # 먼저 원본 텍스트로 파싱 시도 (strict=False로 제어 문자 허용)
            try:
                data = json.loads(text, strict=False)
            except json.JSONDecodeError:
                # 파싱 실패 시 제어 문자 제거 후 재시도
                # 제어 문자만 제거
                text_cleaned = re.sub(r"[\x00-\x1f\x7f]", "", text)
                data = json.loads(text_cleaned)

            if isinstance(data, dict):
                # choice_index가 있으면 인덱스를 직접 사용
                if "choice_index" in data and isinstance(data["choice_index"], int):
                    index = data["choice_index"]
                    if 0 <= index < len(choices):
                        return choices[index], index, data.get("confidence", 1.0)
                    else:
                        logger.warning(f"Invalid choice_index {index} for {len(choices)} choices")

                # choice_index가 없으면 기존 방식 사용
                if "choice" in data:
                    choice = data["choice"]
                    # choice 값에서 제어 문자 제거
                    # 예: "\u001cA/S\u001d요청" → "A/S요청"
                    choice = re.sub(r"[\x00-\x1f\x7f]", "", choice)

                    # 디버깅용 로그
                    logger.debug(f"Original choice: {repr(data['choice'])}")
                    logger.debug(f"Cleaned choice: {repr(choice)}")
                    logger.debug(f"Available choices: {choices}")

                    # choices에서 정확한 매칭 찾기
                    if choice in choices:
                        return choice, choices.index(choice), data.get("confidence", 1.0)

                    # 부분 매칭 시도 (제어 문자로 인해 잘린 경우)
                    for i, candidate in enumerate(choices):
                        # 양방향 부분 매칭 확인
                        if candidate.startswith(choice) or choice in candidate:
                            logger.debug(f"Partial match found: '{choice}' -> '{candidate}'")
                            return candidate, i, data.get("confidence", 0.8)
                        # 반대 방향도 확인 (choice가 candidate보다 긴 경우)
                        if choice.startswith(candidate):
                            logger.debug(f"Reverse partial match found: '{choice}' -> '{candidate}'")
                            return candidate, i, data.get("confidence", 0.7)

        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        # 텍스트 매칭
        text_clean = text.strip()

        # 정확한 매칭
        if text_clean in choices:
            return text_clean, choices.index(text_clean), 1.0

        # 대소문자 무시 매칭
        text_lower = text_clean.lower()
        for i, choice in enumerate(choices):
            if choice.lower() == text_lower:
                return choice, i, 0.9

        # 부분 매칭
        for i, choice in enumerate(choices):
            if choice in text_clean or text_clean in choice:
                logger.warning("Partial match found. Response: '%s', Matched: '%s'", text_clean, choice)
                return choice, i, 0.7

        # choices_optional이 True이고 "None of the above"가 포함된 경우
        if choices_optional and ("none of the above" in text_lower or "해당 없음" in text_clean):
            return None, None, 0.8

        # 매칭 실패
        logger.warning("No valid choice found in response: %s", text_clean)
        return None, None, 0.0

    def _process_schema_response(
        self, text: str, schema: Type["BaseModel"]
    ) -> tuple[Optional["BaseModel"], Optional[list[str]]]:
        """
        응답 텍스트를 스키마에 맞게 파싱하고 검증

        Returns:
            (parsed_model, validation_errors) 튜플
        """
        import json
        import re

        # 마크다운 코드 블록 제거
        text = text.strip()

        # ```json ... ``` 패턴 매칭
        json_block_pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
        match = re.search(json_block_pattern, text, re.DOTALL)
        if match:
            text = match.group(1).strip()

        try:
            # JSON 파싱 시도
            data = json.loads(text)

            # Pydantic 모델로 검증
            model_instance = schema(**data)
            return model_instance, None

        except json.JSONDecodeError as e:
            # JSON 파싱 실패
            error_msg = f"JSON parsing failed: {str(e)}"
            logger.warning(error_msg)
            return None, [error_msg]

        except Exception as e:
            # Pydantic 검증 실패
            error_msg = f"Schema validation failed: {str(e)}"
            logger.warning(error_msg)
            return None, [error_msg]

    @abc.abstractmethod
    def _make_request_params(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: LLMChatModelType,
    ) -> dict:
        pass

    @abc.abstractmethod
    def _make_ask(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: LLMChatModelType,
    ) -> Reply:
        """Generate a response using the specific LLM provider"""
        pass

    @abc.abstractmethod
    async def _make_ask_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: LLMChatModelType,
    ) -> Reply:
        """Generate a response asynchronously using the specific LLM provider"""
        pass

    @abc.abstractmethod
    def _make_ask_stream(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: LLMChatModelType,
    ) -> Generator[Reply, None, None]:
        """Generate a streaming response using the specific LLM provider"""
        yield Reply(text="")

    @abc.abstractmethod
    async def _make_ask_stream_async(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: LLMChatModelType,
    ) -> AsyncGenerator[Reply, None]:
        """Generate a streaming response asynchronously using the specific LLM provider"""
        yield Reply(text="")

    def _ask_impl(
        self,
        input: Union[str, dict[str, str]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[LLMChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        schema: Optional[Type["BaseModel"]] = None,
        is_async: bool = False,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        include_raw_response: Optional[bool] = None,
    ):
        """동기 또는 비동기 응답을 생성하는 내부 메서드 (일반/스트리밍)"""
        # stateless 모드에서는 use_history를 무시
        if self.stateless and use_history:
            logger.debug("stateless 모드에서는 use_history=True가 무시됩니다.")
            use_history = False

        current_messages = [*self.history] if use_history else []
        current_model: LLMChatModelType = cast(LLMChatModelType, model or self.model)

        # Tracing setup
        tracer = None
        if self.enable_tracing:
            try:
                from pyhub.llm.tracing import SpanKind, get_tracer

                tracer = get_tracer()
            except ImportError:
                logger.debug("Tracing requested but pyhub.llm.tracing not available")

        # Determine if we should trace this operation
        should_trace = tracer is not None and self.enable_tracing

        if isinstance(input, dict):
            input_context = input
        else:
            input_context = {}

        if context:
            input_context.update(context)

        # cache 객체가 있으면 캐시 사용
        input_context["enable_cache"] = self.cache is not None

        # include_raw_response 처리
        if include_raw_response is None:
            if self.include_raw_response is not None:
                include_raw_response = self.include_raw_response
            else:
                include_raw_response = False
        input_context["include_raw_response"] = include_raw_response

        # choices 처리
        if choices:
            if len(choices) < 2:
                raise ValueError("choices must contain at least 2 items")

            # choices_optional이 True면 None 옵션 추가
            internal_choices = choices.copy()
            if choices_optional:
                internal_choices.append("None of the above")

            # choices 관련 컨텍스트 추가
            input_context["choices"] = internal_choices  # 원본 그대로 전달
            input_context["choices_formatted"] = "\n".join([f"{i+1}. {c}" for i, c in enumerate(internal_choices)])
            input_context["choices_optional"] = choices_optional

        # schema 처리
        if schema:
            input_context["schema"] = schema
            input_context["schema_json"] = schema.model_json_schema()

        human_prompt = self.get_human_prompt(input, input_context)
        human_message = Message(role="user", content=human_prompt, files=files)

        # 스트리밍 응답 처리
        if stream:

            async def async_stream_handler() -> AsyncGenerator[Reply, None]:
                try:
                    text_list = []
                    async for ask in self._make_ask_stream_async(
                        input_context=input_context,
                        human_message=human_message,
                        messages=current_messages,
                        model=current_model,
                    ):
                        text_list.append(ask.text)
                        yield ask

                    # 스트리밍 완료 후 choices 처리
                    if choices and text_list:
                        full_text = "".join(text_list)
                        choice, index, confidence = self._process_choice_response(
                            full_text, input_context["choices"], choices_optional
                        )
                        # 마지막에 choice 정보를 포함한 Reply 전송
                        yield Reply(text="", choice=choice, choice_index=index, confidence=confidence)

                    # 스트리밍 완료 후 schema 처리
                    if schema and text_list:
                        full_text = "".join(text_list)
                        structured_data, validation_errors = self._process_schema_response(full_text, schema)
                        # 마지막에 structured_data 정보를 포함한 Reply 전송
                        yield Reply(text="", structured_data=structured_data, validation_errors=validation_errors)

                    if use_history:
                        ai_text = "".join(text_list)
                        self._update_history(human_message=human_message, ai_message=ai_text)
                except Exception as e:
                    if raise_errors:
                        raise e
                    yield Reply(text=f"Error: {str(e)}")

            def sync_stream_handler() -> Generator[Reply, None, None]:
                try:
                    text_list = []
                    for ask in self._make_ask_stream(
                        input_context=input_context,
                        human_message=human_message,
                        messages=current_messages,
                        model=current_model,
                    ):
                        text_list.append(ask.text)
                        yield ask

                    # 스트리밍 완료 후 choices 처리
                    if choices and text_list:
                        full_text = "".join(text_list)
                        choice, index, confidence = self._process_choice_response(
                            full_text, input_context["choices"], choices_optional
                        )
                        # 마지막에 choice 정보를 포함한 Reply 전송
                        yield Reply(text="", choice=choice, choice_index=index, confidence=confidence)

                    # 스트리밍 완료 후 schema 처리
                    if schema and text_list:
                        full_text = "".join(text_list)
                        structured_data, validation_errors = self._process_schema_response(full_text, schema)
                        # 마지막에 structured_data 정보를 포함한 Reply 전송
                        yield Reply(text="", structured_data=structured_data, validation_errors=validation_errors)

                    if use_history:
                        ai_text = "".join(text_list)
                        self._update_history(human_message=human_message, ai_message=ai_text)
                except Exception as e:
                    if raise_errors:
                        raise e
                    yield Reply(text=f"Error: {str(e)}")

            return async_stream_handler() if is_async else sync_stream_handler()

        # 일반 응답 처리
        else:

            async def async_handler() -> Reply:
                if should_trace:
                    # Async with tracing
                    with tracer.trace(
                        name=f"{self.__class__.__name__}.ask",
                        kind=SpanKind.LLM,
                        inputs={
                            "prompt": str(input)[:1000],
                            "temperature": self.temperature,
                            "max_tokens": self.max_tokens,
                        },
                        model=str(current_model),
                        tags=["llm", self.__class__.__name__.lower()],
                    ) as span:
                        try:
                            ask = await self._make_ask_async(
                                input_context=input_context,
                                human_message=human_message,
                                messages=current_messages,
                                model=current_model,
                            )

                            # Capture token usage
                            if hasattr(self, "_last_usage") and self._last_usage:
                                span.prompt_tokens = self._last_usage.get("prompt_tokens")
                                span.completion_tokens = self._last_usage.get("completion_tokens")
                                span.total_tokens = self._last_usage.get("total_tokens")

                            # Capture output
                            span.outputs["text"] = ask.text[:1000]
                            if ask.raw_response:
                                span.metadata["raw_response"] = str(ask.raw_response)[:500]

                        except Exception as e:
                            span.error = e
                            if raise_errors:
                                raise e
                            return Reply(text=f"Error: {str(e)}")
                        else:
                            # choices가 있으면 처리
                            if choices:
                                choice, index, confidence = self._process_choice_response(
                                    ask.text, input_context["choices"], choices_optional
                                )
                                ask.choice = choice
                                ask.choice_index = index
                                ask.confidence = confidence

                            # schema가 있으면 처리
                            if schema:
                                structured_data, validation_errors = self._process_schema_response(ask.text, schema)
                                ask.structured_data = structured_data
                                ask.validation_errors = validation_errors

                            if use_history:
                                self._update_history(human_message=human_message, ai_message=ask.text)
                            return ask
                else:
                    # Async without tracing (original implementation)
                    try:
                        ask = await self._make_ask_async(
                            input_context=input_context,
                            human_message=human_message,
                            messages=current_messages,
                            model=current_model,
                        )
                    except Exception as e:
                        if raise_errors:
                            raise e
                        return Reply(text=f"Error: {str(e)}")
                    else:
                        # choices가 있으면 처리
                        if choices:
                            choice, index, confidence = self._process_choice_response(
                                ask.text, input_context["choices"], choices_optional
                            )
                            ask.choice = choice
                            ask.choice_index = index
                            ask.confidence = confidence

                        # schema가 있으면 처리
                        if schema:
                            structured_data, validation_errors = self._process_schema_response(ask.text, schema)
                            ask.structured_data = structured_data
                            ask.validation_errors = validation_errors

                        if use_history:
                            self._update_history(human_message=human_message, ai_message=ask.text)
                        return ask

            def sync_handler() -> Reply:
                if should_trace:
                    # Sync with tracing
                    with tracer.trace(
                        name=f"{self.__class__.__name__}.ask",
                        kind=SpanKind.LLM,
                        inputs={
                            "prompt": str(input)[:1000],
                            "temperature": self.temperature,
                            "max_tokens": self.max_tokens,
                        },
                        model=str(current_model),
                        tags=["llm", self.__class__.__name__.lower()],
                    ) as span:
                        try:
                            ask = self._make_ask(
                                input_context=input_context,
                                human_message=human_message,
                                messages=current_messages,
                                model=current_model,
                            )

                            # Capture token usage
                            if hasattr(self, "_last_usage") and self._last_usage:
                                span.prompt_tokens = self._last_usage.get("prompt_tokens")
                                span.completion_tokens = self._last_usage.get("completion_tokens")
                                span.total_tokens = self._last_usage.get("total_tokens")

                            # Capture output
                            span.outputs["text"] = ask.text[:1000]
                            if ask.raw_response:
                                span.metadata["raw_response"] = str(ask.raw_response)[:500]

                        except Exception as e:
                            span.error = e
                            if raise_errors:
                                raise e
                            return Reply(text=f"Error: {str(e)}")
                        else:
                            # choices가 있으면 처리
                            if choices:
                                choice, index, confidence = self._process_choice_response(
                                    ask.text, input_context["choices"], choices_optional
                                )
                                ask.choice = choice
                                ask.choice_index = index
                                ask.confidence = confidence

                            # schema가 있으면 처리
                            if schema:
                                structured_data, validation_errors = self._process_schema_response(ask.text, schema)
                                ask.structured_data = structured_data
                                ask.validation_errors = validation_errors

                            if use_history:
                                self._update_history(human_message=human_message, ai_message=ask.text)
                            return ask
                else:
                    # Sync without tracing (original implementation)
                    try:
                        ask = self._make_ask(
                            input_context=input_context,
                            human_message=human_message,
                            messages=current_messages,
                            model=current_model,
                        )
                    except Exception as e:
                        if raise_errors:
                            raise e
                        return Reply(text=f"Error: {str(e)}")
                    else:
                        # choices가 있으면 처리
                        if choices:
                            choice, index, confidence = self._process_choice_response(
                                ask.text, input_context["choices"], choices_optional
                            )
                            ask.choice = choice
                            ask.choice_index = index
                            ask.confidence = confidence

                        # schema가 있으면 처리
                        if schema:
                            structured_data, validation_errors = self._process_schema_response(ask.text, schema)
                            ask.structured_data = structured_data
                            ask.validation_errors = validation_errors

                        if use_history:
                            self._update_history(human_message=human_message, ai_message=ask.text)
                        return ask

            return async_handler() if is_async else sync_handler()

    def invoke(
        self,
        input: Union[str, dict[str, str]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        stream: bool = False,
        raise_errors: bool = False,
    ) -> Reply:
        """langchain 호환 메서드: 동기적으로 LLM에 메시지를 전송하고 응답을 반환합니다."""
        return self.ask(input=input, files=files, stream=stream, raise_errors=raise_errors)

    def stream(
        self,
        input: Union[str, dict[str, str]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        raise_errors: bool = False,
    ) -> Generator[Reply, None, None]:
        """langchain 호환 메서드: 동기적으로 LLM에 메시지를 전송하고 응답을 스트리밍합니다."""
        return self.ask(input=input, files=files, stream=True, raise_errors=raise_errors)

    def ask(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[LLMChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        schema: Optional[Type["BaseModel"]] = None,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
        include_raw_response: Optional[bool] = None,
    ) -> Union[Reply, Generator[Reply, None, None]]:
        # schema와 choices는 동시에 사용할 수 없음
        if schema and choices:
            raise ValueError("Cannot use both 'schema' and 'choices' parameters at the same time")

        # 기본 도구와 ask 도구를 합침
        merged_tools = self._merge_tools(tools)

        # 도구가 있으면 도구와 함께 처리
        if merged_tools:
            return self._ask_with_tools(
                input=input,
                files=files,
                model=model,
                context=context,
                tools=merged_tools,
                tool_choice=tool_choice,
                max_tool_calls=max_tool_calls,
                choices=choices,
                choices_optional=choices_optional,
                stream=stream,
                use_history=use_history,
                raise_errors=raise_errors,
                is_async=False,
            )
        else:
            return self._ask_impl(
                input=input,
                files=files,
                model=model,
                context=context,
                choices=choices,
                choices_optional=choices_optional,
                schema=schema,
                is_async=False,
                stream=stream,
                use_history=use_history,
                raise_errors=raise_errors,
                include_raw_response=include_raw_response,
            )

    async def ask_async(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[LLMChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        *,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        schema: Optional[Type["BaseModel"]] = None,
        stream: bool = False,
        raise_errors: bool = False,
        use_history: bool = True,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
        include_raw_response: Optional[bool] = None,
    ) -> Union[Reply, AsyncGenerator[Reply, None]]:
        # schema와 choices는 동시에 사용할 수 없음
        if schema and choices:
            raise ValueError("Cannot use both 'schema' and 'choices' parameters at the same time")

        # 기본 도구와 ask 도구를 합침
        merged_tools = self._merge_tools(tools)

        # 도구가 있으면 도구와 함께 처리
        if merged_tools:
            return_value = self._ask_with_tools(
                input=input,
                files=files,
                model=model,
                context=context,
                tools=merged_tools,
                tool_choice=tool_choice,
                max_tool_calls=max_tool_calls,
                choices=choices,
                choices_optional=choices_optional,
                stream=stream,
                use_history=use_history,
                raise_errors=raise_errors,
                is_async=True,
            )
        else:
            return_value = self._ask_impl(
                input=input,
                files=files,
                model=model,
                context=context,
                choices=choices,
                choices_optional=choices_optional,
                schema=schema,
                is_async=True,
                stream=stream,
                use_history=use_history,
                raise_errors=raise_errors,
                include_raw_response=include_raw_response,
            )

        if stream:
            return return_value
        return await return_value

    #
    # Function Calling & Tool Support
    #

    def _merge_tools(self, ask_tools: Optional[list]) -> list:
        """기본 도구와 ask 시 제공된 도구를 합칩니다.

        Args:
            ask_tools: ask 호출 시 제공된 도구들

        Returns:
            합쳐진 도구 리스트 (중복시 ask_tools가 우선)
        """
        # tools 모듈을 동적 import (순환 import 방지)
        from .tools import ToolAdapter

        # 1. 기본 tools로 시작 (name을 키로 하는 딕셔너리)
        merged = {tool.name: tool for tool in self.default_tools}

        # 2. ask tools 추가 (중복시 덮어씀)
        if ask_tools:
            adapted_ask_tools = ToolAdapter.adapt_tools(ask_tools)
            for tool in adapted_ask_tools:
                merged[tool.name] = tool

        return list(merged.values())

    def _ask_with_tools(
        self,
        input: Union[str, dict[str, Any]],
        files: Optional[list[Union[str, Path, IO]]] = None,
        model: Optional[LLMChatModelType] = None,
        context: Optional[dict[str, Any]] = None,
        tools: Optional[list] = None,
        tool_choice: str = "auto",
        max_tool_calls: int = 5,
        choices: Optional[list[str]] = None,
        choices_optional: bool = False,
        stream: bool = False,
        use_history: bool = True,
        raise_errors: bool = False,
        is_async: bool = False,
    ):
        """도구와 함께 LLM 호출을 처리합니다.

        Args:
            tools: 이미 Tool 객체로 변환된 도구들의 리스트
        """
        # tools 모듈을 동적 import (순환 import 방지)
        from .tools import ToolExecutor

        # tools는 이미 _merge_tools에서 Tool 객체로 변환됨
        adapted_tools = tools

        # 도구 실행기 준비
        executor = ToolExecutor(adapted_tools)

        # Provider별 도구 스키마 변환 (하위 클래스에서 구현)
        provider_tools = self._convert_tools_for_provider(adapted_tools)

        if is_async:
            return self._ask_with_tools_async(
                input,
                files,
                model,
                context,
                adapted_tools,
                provider_tools,
                executor,
                tool_choice,
                max_tool_calls,
                choices,
                choices_optional,
                stream,
                use_history,
                raise_errors,
            )
        else:
            return self._ask_with_tools_sync(
                input,
                files,
                model,
                context,
                adapted_tools,
                provider_tools,
                executor,
                tool_choice,
                max_tool_calls,
                choices,
                choices_optional,
                stream,
                use_history,
                raise_errors,
            )

    def _ask_with_tools_sync(
        self,
        input,
        files,
        model,
        context,
        adapted_tools,
        provider_tools,
        executor,
        tool_choice,
        max_tool_calls,
        choices,
        choices_optional,
        stream,
        use_history,
        raise_errors,
    ):
        """동기 버전의 도구 호출 처리"""
        # Trace 시작
        if llm_settings.trace_function_calls:
            print("🔍 [TRACE] Function Calling 시작")
            print(f"   입력: {input}")
            print(f"   사용 가능한 도구: {[tool.name for tool in adapted_tools]}")
            print(f"   최대 호출 횟수: {max_tool_calls}")

        # 초기 메시지 준비
        current_messages = [*self.history] if use_history else []
        human_prompt = self.get_human_prompt(input, context or {})

        # 도구 호출 기록을 위한 리스트
        tool_interactions = []

        # 도구 호출 반복
        for call_count in range(max_tool_calls):
            try:
                if llm_settings.trace_function_calls:
                    print(f"\n📞 [TRACE] LLM 호출 #{call_count + 1}")

                # LLM 호출 (도구 포함)
                response = self._make_ask_with_tools_sync(
                    human_prompt if call_count == 0 else None,
                    current_messages,
                    provider_tools,
                    tool_choice,
                    model,
                    files if call_count == 0 else None,
                )

                # 도구 호출 추출
                tool_calls = self._extract_tool_calls_from_response(response)

                if llm_settings.trace_function_calls:
                    if tool_calls:
                        print(f"   LLM이 요청한 도구 호출: {len(tool_calls)}개")
                        for i, call in enumerate(tool_calls):
                            print(f"     {i+1}. {call['name']}({call['arguments']})")
                    else:
                        print(f"   도구 호출 없음, 최종 응답: {response.text[:100]}...")

                # 도구 호출이 없으면 완료
                if not tool_calls:
                    if llm_settings.trace_function_calls:
                        print(f"✅ [TRACE] Function Calling 완료 (총 {call_count + 1}회 호출)")
                    if use_history and call_count == 0:
                        human_message = Message(role="user", content=human_prompt, files=files)
                        self._update_history(
                            human_message,
                            response.text,
                            tool_interactions=tool_interactions if tool_interactions else None,
                        )
                    return response

                # 도구 실행
                if llm_settings.trace_function_calls:
                    print("\n🛠️  [TRACE] 도구 실행 중...")

                for tool_call in tool_calls:
                    try:
                        if llm_settings.trace_function_calls:
                            # 인자를 더 읽기 쉽게 포맷팅
                            args_str = ", ".join([f"{k}={v}" for k, v in tool_call["arguments"].items()])
                            print(f"   실행: {tool_call['name']}({args_str})")

                        result = executor.execute_tool(tool_call["name"], tool_call["arguments"])

                        if llm_settings.trace_function_calls:
                            print(f"   결과: {result}")

                        # 도구 호출 기록
                        tool_interactions.append(
                            {"tool": tool_call["name"], "arguments": tool_call["arguments"], "result": str(result)}
                        )

                        # 도구 결과를 메시지에 추가
                        current_messages.append(Message(role="assistant", content=f"[Tool Call: {tool_call['name']}]"))
                        current_messages.append(Message(role="user", content=f"[Tool Result: {result}]"))
                    except Exception as e:
                        if llm_settings.trace_function_calls:
                            print(f"   ❌ 오류: {str(e)}")
                        if raise_errors:
                            raise e
                        error_msg = f"Tool execution error: {str(e)}"
                        # 에러도 기록
                        tool_interactions.append(
                            {"tool": tool_call["name"], "arguments": tool_call["arguments"], "error": str(e)}
                        )
                        current_messages.append(Message(role="user", content=f"[Tool Error: {error_msg}]"))

                # 첫 번째 호출이면 히스토리에 추가
                if use_history and call_count == 0:
                    human_message = Message(role="user", content=human_prompt, files=files)
                    current_messages.insert(0, human_message)

            except Exception as e:
                if raise_errors:
                    raise e
                return Reply(text=f"Error in tool processing: {str(e)}")

        # 최대 호출 횟수에 도달한 경우 최종 응답
        try:
            # 마지막 메시지를 human_message로 사용
            if current_messages:
                final_human_message = current_messages[-1]
                final_messages = current_messages[:-1]
            else:
                final_human_message = Message(role="user", content="", files=files)
                final_messages = []

            final_response = self._make_ask(
                input_context={},
                human_message=final_human_message,
                messages=final_messages,
                model=model,
            )

            # 최종 응답에 tool_interactions 추가
            if use_history and tool_interactions:
                # 첫 번째 사용자 메시지와 최종 응답을 히스토리에 추가
                original_human_msg = Message(role="user", content=human_prompt, files=files)
                self._update_history(original_human_msg, final_response.text, tool_interactions=tool_interactions)

            return final_response
        except Exception as e:
            if raise_errors:
                raise e
            return Reply(text=f"Final response error: {str(e)}")

    async def _ask_with_tools_async(
        self,
        input,
        files,
        model,
        context,
        adapted_tools,
        provider_tools,
        executor,
        tool_choice,
        max_tool_calls,
        choices,
        choices_optional,
        stream,
        use_history,
        raise_errors,
    ):
        """비동기 버전의 도구 호출 처리"""
        # 초기 메시지 준비
        current_messages = [*self.history] if use_history else []
        human_prompt = self.get_human_prompt(input, context or {})

        # 도구 호출 기록을 위한 리스트
        tool_interactions = []

        # 도구 호출 반복
        for call_count in range(max_tool_calls):
            try:
                # LLM 호출 (도구 포함)
                response = await self._make_ask_with_tools_async(
                    human_prompt if call_count == 0 else None,
                    current_messages,
                    provider_tools,
                    tool_choice,
                    model,
                    files if call_count == 0 else None,
                )

                # 도구 호출 추출
                tool_calls = self._extract_tool_calls_from_response(response)

                # 도구 호출이 없으면 완료
                if not tool_calls:
                    if use_history and call_count == 0:
                        human_message = Message(role="user", content=human_prompt, files=files)
                        self._update_history(
                            human_message,
                            response.text,
                            tool_interactions=tool_interactions if tool_interactions else None,
                        )
                    return response

                # 도구 실행
                for tool_call in tool_calls:
                    try:
                        result = await executor.execute_tool_async(tool_call["name"], tool_call["arguments"])

                        # 도구 호출 기록
                        tool_interactions.append(
                            {"tool": tool_call["name"], "arguments": tool_call["arguments"], "result": str(result)}
                        )

                        # 도구 결과를 메시지에 추가
                        current_messages.append(Message(role="assistant", content=f"[Tool Call: {tool_call['name']}]"))
                        current_messages.append(Message(role="user", content=f"[Tool Result: {result}]"))
                    except Exception as e:
                        if raise_errors:
                            raise e
                        error_msg = f"Tool execution error: {str(e)}"
                        # 에러도 기록
                        tool_interactions.append(
                            {"tool": tool_call["name"], "arguments": tool_call["arguments"], "error": str(e)}
                        )
                        current_messages.append(Message(role="user", content=f"[Tool Error: {error_msg}]"))

                # 첫 번째 호출이면 히스토리에 추가
                if use_history and call_count == 0:
                    human_message = Message(role="user", content=human_prompt, files=files)
                    current_messages.insert(0, human_message)

            except Exception as e:
                if raise_errors:
                    raise e
                return Reply(text=f"Error in tool processing: {str(e)}")

        # 최대 호출 횟수에 도달한 경우 최종 응답
        try:
            # 마지막 메시지를 human_message로 사용
            if current_messages:
                final_human_message = current_messages[-1]
                final_messages = current_messages[:-1]
            else:
                final_human_message = Message(role="user", content="", files=files)
                final_messages = []

            final_response = await self._make_ask_async(
                input_context={},
                human_message=final_human_message,
                messages=final_messages,
                model=model,
            )

            # 최종 응답에 tool_interactions 추가
            if use_history and tool_interactions:
                # 첫 번째 사용자 메시지와 최종 응답을 히스토리에 추가
                original_human_msg = Message(role="user", content=human_prompt, files=files)
                self._update_history(original_human_msg, final_response.text, tool_interactions=tool_interactions)

            return final_response
        except Exception as e:
            if raise_errors:
                raise e
            return Reply(text=f"Final response error: {str(e)}")

    def _convert_tools_for_provider(self, tools):
        """Provider별 도구 스키마 변환 (하위 클래스에서 구현)"""
        # 기본적으로 빈 리스트 반환 (Function Calling 미지원)
        return []

    def _extract_tool_calls_from_response(self, response):
        """응답에서 도구 호출 정보 추출 (하위 클래스에서 구현)"""
        # 기본적으로 빈 리스트 반환
        return []

    def _make_ask_with_tools_sync(self, human_prompt, messages, tools, tool_choice, model, files):
        """도구와 함께 동기 LLM 호출 (하위 클래스에서 구현)"""
        # 기본적으로 일반 ask 호출
        return self._make_ask(
            input_context={},
            human_message=Message(role="user", content=human_prompt or ""),
            messages=messages,
            model=model,
        )

    async def _make_ask_with_tools_async(self, human_prompt, messages, tools, tool_choice, model, files):
        """도구와 함께 비동기 LLM 호출 (하위 클래스에서 구현)"""
        # 기본적으로 일반 ask 호출
        return await self._make_ask_async(
            input_context={},
            human_message=Message(role="user", content=human_prompt or ""),
            messages=messages,
            model=model,
        )

    #
    # embed
    #
    def get_embed_size(self, model: Optional[LLMEmbeddingModelType] = None) -> int:
        return self.EMBEDDING_DIMENSIONS[model or self.embedding_model]

    @property
    def embed_size(self) -> int:
        return self.get_embed_size()

    @abc.abstractmethod
    def embed(
        self,
        input: Union[str, list[str]],
        model: Optional[LLMEmbeddingModelType] = None,
    ) -> Union[Embed, EmbedList]:
        pass

    @abc.abstractmethod
    async def embed_async(
        self,
        input: Union[str, list[str]],
        model: Optional[LLMEmbeddingModelType] = None,
    ) -> Union[Embed, EmbedList]:
        pass

    @abc.abstractmethod
    def generate_image(
        self,
        prompt: str,
        *,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: Optional[str] = None,
        n: int = 1,
        response_format: str = "url",
        **kwargs,
    ) -> "ImageReply":
        """Generate images from text prompts.

        Args:
            prompt: The text prompt to generate images from
            size: Image size (e.g., "1024x1024", "1024x1792", "1792x1024")
            quality: Image quality ("standard" or "hd")
            style: Image style ("vivid" or "natural")
            n: Number of images to generate
            response_format: Format of the response ("url" or "base64")
            **kwargs: Additional provider-specific parameters

        Returns:
            ImageReply: Generated image response

        Raises:
            NotImplementedError: If the provider doesn't support image generation
            ValueError: If the model doesn't support image generation or invalid parameters
        """
        pass

    @abc.abstractmethod
    async def generate_image_async(
        self,
        prompt: str,
        *,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: Optional[str] = None,
        n: int = 1,
        response_format: str = "url",
        **kwargs,
    ) -> "ImageReply":
        """Asynchronously generate images from text prompts.

        Args:
            prompt: The text prompt to generate images from
            size: Image size (e.g., "1024x1024", "1024x1792", "1792x1024")
            quality: Image quality ("standard" or "hd")
            style: Image style ("vivid" or "natural")
            n: Number of images to generate
            response_format: Format of the response ("url" or "base64")
            **kwargs: Additional provider-specific parameters

        Returns:
            ImageReply: Generated image response

        Raises:
            NotImplementedError: If the provider doesn't support image generation
            ValueError: If the model doesn't support image generation or invalid parameters
        """
        pass

    def supports(self, capability: str) -> bool:
        """Check if the current model supports a specific capability.

        Args:
            capability: The capability to check (e.g., "image_generation")

        Returns:
            bool: True if the capability is supported
        """
        # Default implementation - subclasses should override
        return False

    def get_supported_image_sizes(self) -> list[str]:
        """Get the list of supported image sizes for the current model.

        Returns:
            list[str]: List of supported sizes, empty if image generation not supported
        """
        # Default implementation - subclasses should override
        return []

    @property
    def capabilities(self) -> dict[str, Any]:
        """Get the capabilities of the current model.

        Returns:
            dict: Dictionary of capabilities and their details
        """
        # Default implementation - subclasses should override
        return {}

    #
    # MCP (Model Context Protocol) integration
    #

    async def initialize_mcp(self) -> None:
        """MCP 서버들을 연결하고 도구를 로드합니다."""
        if not self.mcp_servers:
            return

        if self._mcp_connected:
            logger.warning("MCP is already connected")
            return

        try:
            # MCP 모듈을 동적 import
            from .mcp import MultiServerMCPClient
            from .mcp.policies import MCPConnectionError, MCPConnectionPolicy

            # 기본 정책 설정
            if self.mcp_policy is None:
                self.mcp_policy = MCPConnectionPolicy.OPTIONAL

            # MultiServerMCPClient 생성
            self._mcp_client = MultiServerMCPClient(self.mcp_servers)

            # 연결 시작
            await self._mcp_client.__aenter__()

            # 연결 실패 확인
            failed_servers = list(self._mcp_client._connection_errors.keys())
            if failed_servers:
                # 정책에 따른 처리
                if self.mcp_policy == MCPConnectionPolicy.REQUIRED:
                    # REQUIRED: 예외 발생
                    error_msg = f"Failed to connect to MCP servers: {', '.join(failed_servers)}"
                    await self.close_mcp()  # 정리
                    raise MCPConnectionError(error_msg, failed_servers)
                elif self.mcp_policy == MCPConnectionPolicy.WARN:
                    # WARN: 경고 로그
                    logger.warning(f"Failed to connect to some MCP servers: {', '.join(failed_servers)}")
                # OPTIONAL: 조용히 계속 진행

            # 도구 로드
            self._mcp_tools = await self._mcp_client.get_tools()

            # 기존 도구와 병합
            from .tools import ToolAdapter

            if self._mcp_tools:
                adapted_mcp_tools = ToolAdapter.adapt_tools(self._mcp_tools)
                self.default_tools.extend(adapted_mcp_tools)
                logger.info(f"Loaded {len(self._mcp_tools)} MCP tools from {len(self.mcp_servers)} servers")

            self._mcp_connected = True

        except MCPConnectionError:
            # 정책에 따른 예외는 다시 발생
            raise
        except Exception as e:
            # 기타 예외 처리
            if self.mcp_policy == MCPConnectionPolicy.REQUIRED:
                error_msg = f"Failed to initialize MCP: {e}"
                await self.close_mcp()  # 정리
                raise MCPConnectionError(error_msg)
            else:
                logger.error(f"Failed to initialize MCP: {e}")
                # MCP 연결 실패는 치명적이지 않으므로 계속 진행
                self._mcp_client = None
                self._mcp_connected = False

    async def close_mcp(self, timeout: float = 5.0) -> None:
        """MCP 연결을 종료합니다.

        Args:
            timeout: 종료 대기 시간 (초)
        """
        if self._mcp_client and self._mcp_connected:
            try:
                # 타임아웃 적용
                await asyncio.wait_for(self._mcp_client.__aexit__(None, None, None), timeout=timeout)
                logger.info("MCP connections closed")
            except asyncio.TimeoutError:
                logger.warning(f"MCP cleanup timed out after {timeout}s")
            except Exception as e:
                logger.error(f"Error closing MCP connections: {e}")
            finally:
                self._mcp_client = None
                self._mcp_connected = False

                # MCP 도구 제거
                if self._mcp_tools:
                    # 기존 도구에서 MCP 도구 제거
                    from .tools import ToolAdapter

                    adapted_mcp_tools = ToolAdapter.adapt_tools(self._mcp_tools)
                    for tool in adapted_mcp_tools:
                        if tool in self.default_tools:
                            self.default_tools.remove(tool)
                    self._mcp_tools = []

    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.initialize_mcp()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.close_mcp()
        return False

    #
    # describe images / tables
    #

    def describe_images(
        self,
        images: Union[
            Union[str, Path, IO], list[Union[str, Path, IO]], DescribeImageRequest, list[DescribeImageRequest]
        ],
        prompt: Optional[str] = None,
        *,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_parallel_size: int = 4,
        raise_errors: bool = False,
        use_history: bool = False,
    ) -> Union[Reply, list[Reply]]:
        """
        여러 이미지를 병렬로 처리하여 설명을 생성합니다.

        Args:
            images: 이미지 파일 경로(들) 또는 DescribeImageRequest 객체(들)
            prompt: 모든 이미지에 적용할 프롬프트 (DescribeImageRequest 사용시 무시됨)
            system_prompt: 시스템 프롬프트 (선택사항)
            temperature: 생성 온도 (선택사항)
            max_tokens: 최대 토큰 수 (선택사항)
            max_parallel_size: 최대 병렬 처리 개수 (기본값: 4)
            raise_errors: 에러 발생시 예외를 발생시킬지 여부
            enable_cache: 캐싱 활성화 여부
            use_history: 대화 히스토리 사용 여부 (기본값: False)

        Returns:
            단일 이미지인 경우 Reply, 여러 이미지인 경우 list[Reply]

        Examples:
            # 단일 이미지
            response = llm.describe_images("photo.jpg")

            # 여러 이미지
            responses = llm.describe_images(["img1.jpg", "img2.jpg", "img3.jpg"])

            # 커스텀 프롬프트
            responses = llm.describe_images(
                ["img1.jpg", "img2.jpg"],
                prompt="What objects are in this image?",
                temperature=0.5
            )

            # 기존 DescribeImageRequest 방식도 지원
            request = DescribeImageRequest(...)
            response = llm.describe_images(request)
        """
        return async_to_sync(self.describe_images_async)(
            images,
            prompt,
            system_prompt,
            temperature,
            max_tokens,
            max_parallel_size,
            raise_errors,
            use_history,
        )

    async def describe_images_async(
        self,
        images: Union[
            Union[str, Path, IO], list[Union[str, Path, IO]], DescribeImageRequest, list[DescribeImageRequest]
        ],
        prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_parallel_size: int = 4,
        raise_errors: bool = False,
        use_history: bool = False,
    ) -> Union[Reply, list[Reply]]:
        """여러 이미지를 병렬로 처리하여 설명을 생성합니다 (비동기)"""

        # 입력을 정규화하여 처리할 이미지 리스트 생성
        is_single = False
        if isinstance(images, (DescribeImageRequest, str, Path)) or hasattr(images, "read"):
            is_single = True
            images_list = [images]
        else:
            images_list = list(images)

        # DescribeImageRequest와 일반 이미지를 구분하여 처리
        request_list = []
        for idx, img in enumerate(images_list):
            if isinstance(img, DescribeImageRequest):
                request_list.append(img)
            else:
                # 일반 이미지를 DescribeImageRequest로 변환
                request = DescribeImageRequest(
                    image=img,
                    image_path=str(img) if isinstance(img, (str, Path)) else f"image_{idx}",
                    system_prompt=system_prompt or self.system_prompt,
                    user_prompt=prompt or "Describe this image in detail.",
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                request_list.append(request)

        # 세마포어를 통해 병렬 처리 제한
        semaphore = asyncio.Semaphore(max_parallel_size)

        async def process_single_image(
            task_request: DescribeImageRequest,
            idx: int,
            total: int,
        ) -> Reply:
            async with semaphore:
                logger.info("request describe_images [%d/%d] : %s", idx + 1, total, task_request.image_path)

                # 기존 인스턴스의 설정을 임시로 변경
                original_system_prompt = self.system_prompt
                original_temperature = self.temperature
                original_max_tokens = self.max_tokens

                try:
                    # 요청별 설정 적용
                    if task_request.system_prompt is not None:
                        self.system_prompt = task_request.system_prompt
                    if task_request.temperature is not None:
                        self.temperature = task_request.temperature
                    if task_request.max_tokens is not None:
                        self.max_tokens = task_request.max_tokens

                    # 현재 인스턴스를 사용하여 ask_async 호출
                    reply = await self.ask_async(
                        input=task_request.user_prompt,
                        files=[task_request.image],
                        context=task_request.prompt_context,
                        raise_errors=raise_errors,
                        use_history=use_history,
                    )
                    logger.debug("image description for %s : %s", task_request.image_path, repr(reply.text))
                    return reply

                finally:
                    # 원래 설정 복원
                    self.system_prompt = original_system_prompt
                    self.temperature = original_temperature
                    self.max_tokens = original_max_tokens

        # 병렬로 모든 이미지 처리
        tasks = [process_single_image(request, idx, len(request_list)) for idx, request in enumerate(request_list)]
        reply_list = await asyncio.gather(*tasks)

        # 파일 포인터 리셋 (IO 객체인 경우)
        for request in request_list:
            if hasattr(request.image, "seek"):
                request.image.seek(0)

        # 단일 이미지였으면 Reply 반환, 여러 이미지였으면 list[Reply] 반환
        return reply_list[0] if is_single else reply_list

    def describe_image(
        self,
        image: Union[str, Path, IO],
        prompt: str = "Describe this image in detail.",
        *,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_history: bool = False,
        **kwargs,
    ) -> Reply:
        """
        단일 이미지를 간단하게 설명 요청

        이 메서드는 ask() 메서드의 편의 래퍼입니다.
        대량 이미지 병렬 처리가 필요한 경우 describe_images()를 사용하세요.

        Args:
            image: 이미지 파일 경로, Path 객체, 또는 파일 IO 객체
            prompt: 이미지 설명을 위한 프롬프트 (기본값: "Describe this image in detail.")
            system_prompt: 시스템 프롬프트 (선택사항)
            temperature: 생성 온도 (선택사항)
            max_tokens: 최대 토큰 수 (선택사항)
            enable_cache: 캐싱 활성화 여부
            use_history: 대화 히스토리 사용 여부 (기본값: False)
            **kwargs: ask() 메서드에 전달할 추가 파라미터

        Returns:
            Reply: 이미지 설명이 포함된 응답

        Examples:
            # 기본 사용
            response = llm.describe_image("photo.jpg")

            # 대화 히스토리 포함
            response = llm.describe_image("photo.jpg", use_history=True)

            # ask()와 동일한 결과
            response = llm.ask("Describe this image in detail.", files=["photo.jpg"])
        """
        # 기존 시스템 프롬프트 임시 저장
        original_system_prompt = self.system_prompt

        # 시스템 프롬프트가 제공된 경우 임시로 설정
        if system_prompt is not None:
            self.system_prompt = system_prompt

        try:
            # temperature와 max_tokens 처리
            # 일부 프로바이더는 이를 ask 파라미터로 받지 않으므로 임시로 인스턴스 값 변경
            original_temperature = self.temperature
            original_max_tokens = self.max_tokens

            if temperature is not None:
                self.temperature = temperature
            if max_tokens is not None:
                self.max_tokens = max_tokens

            # ask 메서드 호출
            result = self.ask(input=prompt, files=[image], use_history=use_history, **kwargs)
        finally:
            # 원래 값들 복원
            self.system_prompt = original_system_prompt
            if temperature is not None:
                self.temperature = original_temperature
            if max_tokens is not None:
                self.max_tokens = original_max_tokens

        return result

    async def describe_image_async(
        self,
        image: Union[str, Path, IO],
        prompt: str = "Describe this image in detail.",
        *,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_history: bool = False,
        **kwargs,
    ) -> Reply:
        """
        단일 이미지를 간단하게 설명 요청 (비동기)

        이 메서드는 ask_async() 메서드의 편의 래퍼입니다.

        Args:
            image: 이미지 파일 경로, Path 객체, 또는 파일 IO 객체
            prompt: 이미지 설명을 위한 프롬프트 (기본값: "Describe this image in detail.")
            system_prompt: 시스템 프롬프트 (선택사항)
            temperature: 생성 온도 (선택사항)
            max_tokens: 최대 토큰 수 (선택사항)
            enable_cache: 캐싱 활성화 여부
            use_history: 대화 히스토리 사용 여부 (기본값: False)
            **kwargs: ask_async() 메서드에 전달할 추가 파라미터

        Returns:
            Reply: 이미지 설명이 포함된 응답
        """
        # 기존 시스템 프롬프트 임시 저장
        original_system_prompt = self.system_prompt

        # 시스템 프롬프트가 제공된 경우 임시로 설정
        if system_prompt is not None:
            self.system_prompt = system_prompt

        try:
            # temperature와 max_tokens 처리
            original_temperature = self.temperature
            original_max_tokens = self.max_tokens

            if temperature is not None:
                self.temperature = temperature
            if max_tokens is not None:
                self.max_tokens = max_tokens

            # ask_async 메서드 호출
            result = await self.ask_async(input=prompt, files=[image], use_history=use_history, **kwargs)
        finally:
            # 원래 값들 복원
            self.system_prompt = original_system_prompt
            if temperature is not None:
                self.temperature = original_temperature
            if max_tokens is not None:
                self.max_tokens = original_max_tokens

        return result

    def extract_text_from_image(self, image: Union[str, Path, IO], **kwargs) -> Reply:
        """이미지에서 텍스트 추출 특화 메서드"""
        return self.describe_image(
            image,
            "Extract all text from this image. Return only the text content without any additional explanation.",
            **kwargs,
        )

    def analyze_image_content(self, image: Union[str, Path, IO], **kwargs) -> Reply:
        """이미지 내용 분석 특화 메서드"""
        return self.describe_image(
            image,
            "Analyze this image and provide: 1) Main objects and subjects 2) Dominant colors and visual style 3) Setting or context 4) Any visible text 5) Overall mood or atmosphere",
            **kwargs,
        )

    #
    # Retry and Fallback
    #

    def with_retry(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
        backoff_strategy: Optional[str] = None,
        jitter: bool = True,
        retry_on: Optional[List[Union[Type[Exception], str]]] = None,
        retry_condition: Optional[Callable[[Exception], bool]] = None,
        stop_on: Optional[List[Union[Type[Exception], str]]] = None,
        on_retry: Optional[Callable[[Exception, int, float], None]] = None,
        on_failure: Optional[Callable[[Exception, int], None]] = None,
    ) -> "BaseLLM":
        """Apply retry logic to this LLM instance.

        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay between retries in seconds
            max_delay: Maximum delay between retries
            backoff_multiplier: Multiplier for exponential backoff
            backoff_strategy: One of "exponential", "linear", "fixed", "jitter"
            jitter: Whether to add jitter to delays
            retry_on: List of exceptions or error messages to retry on
            retry_condition: Custom function to determine if an error should be retried
            stop_on: List of exceptions or error messages to not retry on
            on_retry: Callback called on each retry with (error, attempt, delay)
            on_failure: Callback called when all retries fail

        Returns:
            RetryWrapper: A wrapped LLM instance with retry functionality

        Examples:
            # Basic retry with exponential backoff
            llm = OpenAILLM(model="gpt-4o-mini").with_retry(max_retries=3)

            # Custom retry configuration
            llm = OpenAILLM(model="gpt-4o-mini").with_retry(
                max_retries=5,
                initial_delay=0.5,
                backoff_strategy="jitter",
                retry_on=[ConnectionError, "rate limit"],
                on_retry=lambda e, attempt, delay: print(f"Retry {attempt} after {delay}s: {e}")
            )
        """
        from .retry import BackoffStrategy, RetryConfig, RetryWrapper

        # Convert backoff_strategy string to enum if provided
        if backoff_strategy:
            strategy = BackoffStrategy(backoff_strategy)
        else:
            strategy = BackoffStrategy.EXPONENTIAL

        config = RetryConfig(
            max_retries=max_retries,
            initial_delay=initial_delay,
            max_delay=max_delay,
            backoff_factor=backoff_multiplier,
            backoff_strategy=strategy,
            jitter=jitter,
            retry_on=retry_on,
            retry_condition=retry_condition,
            stop_on=stop_on,
            on_retry=on_retry,
            on_failure=on_failure,
        )

        return RetryWrapper(self, config)

    def with_fallbacks(
        self,
        fallback_llms: List["BaseLLM"],
        fallback_condition: Optional[Callable[[Exception], bool]] = None,
        on_fallback: Optional[Callable[[Exception, "BaseLLM"], None]] = None,
    ) -> "BaseLLM":
        """Apply fallback logic to this LLM instance.

        Args:
            fallback_llms: List of LLM instances to use as fallbacks
            fallback_condition: Custom function to determine if an error should trigger fallback
            on_fallback: Callback called when switching to a fallback LLM

        Returns:
            FallbackWrapper: A wrapped LLM instance with fallback functionality

        Examples:
            # Simple fallback chain
            primary = OpenAILLM(model="gpt-4o")
            backup1 = OpenAILLM(model="gpt-4o-mini")
            backup2 = AnthropicLLM(model="claude-3-sonnet")

            llm = primary.with_fallbacks([backup1, backup2])

            # Conditional fallback
            def should_fallback(error):
                return "context length" in str(error).lower()

            llm = primary.with_fallbacks(
                [backup1],
                fallback_condition=should_fallback,
                on_fallback=lambda e, llm: print(f"Switching to {llm.model}: {e}")
            )

            # Combine retry and fallback
            llm = primary.with_retry(max_retries=2).with_fallbacks([backup1, backup2])
        """
        from .retry import FallbackConfig, FallbackWrapper

        config = FallbackConfig(
            fallback_llms=fallback_llms,
            fallback_condition=fallback_condition,
            on_fallback=on_fallback,
        )

        return FallbackWrapper(self, config)


class SequentialChain:
    def __init__(self, *args):
        self.llms: list[BaseLLM] = list(args)

    def insert_first(self, llm) -> "SequentialChain":
        self.llms.insert(0, llm)
        return self

    def append(self, llm) -> "SequentialChain":
        self.llms.append(llm)
        return self

    def ask(self, inputs: dict[str, Any]) -> ChainReply:
        """체인의 각 LLM을 순차적으로 실행합니다. 이전 LLM의 출력이 다음 LLM의 입력으로 전달됩니다."""

        for llm in self.llms:
            if llm.prompt is None:
                raise ValueError(f"prompt is required for LLM: {llm}")

        known_values = inputs.copy()
        reply_list = []
        for llm in self.llms:
            reply = llm.ask(known_values)
            reply_list.append(reply)

            output_key = llm.get_output_key()
            known_values[output_key] = str(reply)

        return ChainReply(
            values=known_values,
            reply_list=reply_list,
        )
