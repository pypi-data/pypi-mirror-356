import logging
from typing import Any, Optional, Union

from pyhub.llm.base import BaseLLM
from pyhub.llm.openai import OpenAIMixin
from pyhub.llm.settings import llm_settings
from pyhub.llm.types import (
    GroundednessCheck,
    ImageReply,
    Message,
    UpstageChatModelType,
    UpstageEmbeddingModelType,
    UpstageGroundednessCheckModel,
    Usage,
)
from pyhub.llm.utils.templates import Template

logger = logging.getLogger(__name__)


class UpstageLLM(OpenAIMixin, BaseLLM):
    EMBEDDING_DIMENSIONS = {
        "embedding-query": 4096,
        "embedding-passage": 4096,
    }
    cache_alias = "upstage"
    supports_stream_options = False  # Upstage doesn't support stream_options

    def __init__(
        self,
        model: UpstageChatModelType = "solar-mini",
        embedding_model: UpstageEmbeddingModelType = "embedding-query",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        prompt: Optional[Union[str, Template]] = None,
        output_key: str = "text",
        initial_messages: Optional[list[Message]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tools: Optional[list] = None,
    ):
        # Lazy import openai (same as OpenAI since Upstage uses OpenAI SDK)
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
            raise ImportError("openai package not installed. " "Install with: pip install pyhub-llm[upstage]")

        super().__init__(
            model=model,
            embedding_model=embedding_model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            prompt=prompt,
            output_key=output_key,
            initial_messages=initial_messages,
            api_key=api_key or llm_settings.upstage_api_key,
            tools=tools,
        )

        self.base_url = base_url or llm_settings.upstage_base_url

    def check(self) -> list[dict]:
        errors = super().check()

        if not self.api_key or not self.api_key.startswith("up_"):
            errors.append(
                {
                    "msg": "Upstage API key is not set or is invalid.",
                    "hint": "Please check your Upstage API key.",
                    "obj": self,
                }
            )

        return errors

    def _make_request_params(
        self,
        input_context: dict[str, Any],
        human_message: Message,
        messages: list[Message],
        model: UpstageChatModelType,
        use_files: bool = False,
    ) -> dict:
        return super()._make_request_params(
            input_context,
            human_message,
            messages,
            model,  # noqa
            use_files=False,
        )

    def is_grounded(
        self,
        model: UpstageGroundednessCheckModel = "groundedness-check",
        raise_errors: bool = False,
    ) -> GroundednessCheck:
        """
        채팅 기록에서 마지막 user/assistant 메시지 쌍에 대해 응답의 근거 검증을 수행합니다.

        마지막 사용자 질문과 AI 응답이 사실에 근거하는지 확인하여 결과를 반환합니다.

        Args:
            model: Upstage의 근거 검증 모델
            raise_errors: 오류 발생 시 예외를 발생시킬지 여부

        Returns:
            Groundedness: 검증 결과 (True: 근거 있음, False: 근거 없음, None: 확실하지 않음)
        """

        # 마지막 user/assistant 쌍에 대해서 검증
        messages = self.history[-2:]

        if len(messages) != 2:
            raise ValueError("Groundedness check requires exactly 2 messages")

        sync_client = self._SyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        try:
            response = sync_client.chat.completions.create(
                model=model,
                messages=messages,
            )
            text = response.choices[0].message.content

            is_grounded = {
                "grounded": True,
                "notGrounded": False,
                "notSure": None,
            }.get(text)

            return GroundednessCheck(
                is_grounded=is_grounded,
                usage=Usage(
                    input=response.usage.prompt_tokens or 0,
                    output=response.usage.completion_tokens or 0,
                ),
            )
        except Exception as e:
            if raise_errors:
                raise e
            logger.error(f"Error occurred during streaming API call: {str(e)}")
            return GroundednessCheck(is_grounded=None, usage=None)

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

        Raises:
            NotImplementedError: Upstage does not support image generation
        """
        raise NotImplementedError(
            "Upstage does not support image generation. "
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
        **kwargs,
    ) -> "ImageReply":
        """Asynchronously generate images from text prompts.

        Raises:
            NotImplementedError: Upstage does not support image generation
        """
        raise NotImplementedError(
            "Upstage does not support image generation. "
            "Please use a provider that supports image generation, such as OpenAI with DALL-E models."
        )
