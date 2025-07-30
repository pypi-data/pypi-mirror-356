from decimal import Decimal
from typing import TYPE_CHECKING, Union, cast

# Always import these as they don't have external dependencies
from pyhub.llm.base import BaseLLM, SequentialChain
from pyhub.llm.display import display, print_stream
from pyhub.llm.mock import MockLLM
from pyhub.llm.types import (
    AnthropicChatModelType,
    GoogleChatModelType,
    GoogleEmbeddingModelType,
    LLMChatModelEnum,
    LLMChatModelType,
    LLMEmbeddingModelEnum,
    LLMEmbeddingModelType,
    LLMModelType,
    LLMVendorType,
    OllamaChatModelType,
    OllamaEmbeddingModelType,
    OpenAIChatModelType,
    OpenAIEmbeddingModelType,
    Price,
    UpstageChatModelType,
    UpstageEmbeddingModelType,
    Usage,
)
from pyhub.llm.utils.type_utils import get_literal_values

# Type checking imports
if TYPE_CHECKING:
    from pyhub.llm.anthropic import AnthropicLLM
    from pyhub.llm.google import GoogleLLM
    from pyhub.llm.ollama import OllamaLLM
    from pyhub.llm.openai import OpenAILLM
    from pyhub.llm.upstage import UpstageLLM


class LLM:
    MODEL_PRICES = {
        # 2025년 3월 기준
        # https://platform.openai.com/docs/pricing#embeddings
        LLMEmbeddingModelEnum.TEXT_EMBEDDING_3_SMALL: ("0.02", None),
        LLMEmbeddingModelEnum.TEXT_EMBEDDING_3_LARGE: ("0.13", None),
        LLMEmbeddingModelEnum.TEXT_EMBEDDING_004: ("0", None),  # 가격 명시 없음.
        # https://platform.openai.com/docs/pricing#latest-models
        LLMChatModelEnum.GPT_4O: ("2.5", "10.0"),
        LLMChatModelEnum.GPT_4O_MINI: ("0.15", "0.60"),
        LLMChatModelEnum.O1: ("15", "60.00"),
        # LLMChatModelEnum.O3_MINI: ("1.10", "4.40"),
        LLMChatModelEnum.O1_MINI: ("1.10", "4.40"),
        # https://www.anthropic.com/pricing#anthropic-api
        # LLMChatModelEnum.CLAUDE_OPUS_4_LATEST: ("15", "75"),
        # LLMChatModelEnum.CLAUDE_SONNET_4_20250514: ("3", "15"),
        LLMChatModelEnum.CLAUDE_SONNET_3_7_LATEST: ("3", "15"),
        LLMChatModelEnum.CLAUDE_HAIKU_3_5_LATEST: ("0.80", "4"),
        LLMChatModelEnum.CLAUDE_OPUS_3_LATEST: ("15", "75"),
        # https://www.upstage.ai/pricing
        LLMChatModelEnum.UPSTAGE_SOLAR_MINI: ("0.15", "0.15"),  # TODO: 가격 확인
        LLMChatModelEnum.UPSTAGE_SOLAR_PRO: ("0.25", "0.15"),
        # https://ai.google.dev/gemini-api/docs/pricing?hl=ko
        LLMChatModelEnum.GEMINI_2_0_FLASH: ("0.10", "0.40"),
        LLMChatModelEnum.GEMINI_2_0_FLASH_LITE: ("0.075", "0.30"),
        LLMChatModelEnum.GEMINI_1_5_FLASH: ("0.075", "0.30"),  # 128,000 토큰 초과 시에는 *2
        LLMChatModelEnum.GEMINI_1_5_FLASH_8B: ("0.0375", "0.15"),  # 128,000 토큰 초과 시에는 *2
        LLMChatModelEnum.GEMINI_1_5_PRO: ("1.25", "5.0"),  # 128,000 토큰 초과 시에는 *2
    }

    @classmethod
    def get_vendor_from_model(cls, model: LLMModelType) -> LLMVendorType:
        """주어진 model로부터 해당하는 vendor를 찾아 반환합니다."""
        if model in get_literal_values(OpenAIChatModelType, OpenAIEmbeddingModelType):
            return "openai"
        elif model in get_literal_values(UpstageChatModelType, UpstageEmbeddingModelType):
            return "upstage"
        elif model in get_literal_values(AnthropicChatModelType):
            return "anthropic"
        elif model in get_literal_values(GoogleChatModelType, GoogleEmbeddingModelType):
            return "google"
        elif model in get_literal_values(OllamaChatModelType, OllamaEmbeddingModelType):
            return "ollama"
        else:
            raise ValueError(f"Unknown model: {model}")

    @classmethod
    def create(
        cls,
        model: LLMModelType,
        **kwargs,
    ) -> "BaseLLM":
        vendor = cls.get_vendor_from_model(model)

        #
        # chat
        #
        if model in get_literal_values(LLMChatModelType):
            if vendor == "openai":
                from pyhub.llm.openai import OpenAILLM

                return OpenAILLM(model=cast(OpenAIChatModelType, model), **kwargs)
            elif vendor == "upstage":
                from pyhub.llm.upstage import UpstageLLM

                return UpstageLLM(model=cast(UpstageChatModelType, model), **kwargs)
            elif vendor == "anthropic":
                from pyhub.llm.anthropic import AnthropicLLM

                return AnthropicLLM(model=cast(AnthropicChatModelType, model), **kwargs)
            elif vendor == "google":
                from pyhub.llm.google import GoogleLLM

                return GoogleLLM(model=cast(GoogleChatModelType, model), **kwargs)
            elif vendor == "ollama":
                from pyhub.llm.ollama import OllamaLLM

                if "max_tokens" in kwargs:
                    del kwargs["max_tokens"]
                return OllamaLLM(model=cast(OllamaChatModelType, model), **kwargs)

        #
        # embedding
        #
        elif model in get_literal_values(LLMEmbeddingModelType):
            if vendor == "openai":
                from pyhub.llm.openai import OpenAILLM

                return OpenAILLM(
                    embedding_model=cast(OpenAIEmbeddingModelType, model),
                    **kwargs,
                )
            elif vendor == "upstage":
                from pyhub.llm.upstage import UpstageLLM

                return UpstageLLM(
                    embedding_model=cast(UpstageEmbeddingModelType, model),
                    **kwargs,
                )
            elif vendor == "google":
                from pyhub.llm.google import GoogleLLM

                return GoogleLLM(
                    embedding_model=cast(GoogleEmbeddingModelType, model),
                    **kwargs,
                )
            elif vendor == "ollama":
                from pyhub.llm.ollama import OllamaLLM

                if "max_tokens" in kwargs:
                    del kwargs["max_tokens"]
                return OllamaLLM(
                    embedding_model=cast(OllamaEmbeddingModelType, model),
                    **kwargs,
                )

        raise ValueError(f"Invalid model name: {model}")

    @classmethod
    async def create_async(
        cls,
        model: LLMModelType,
        **kwargs,
    ) -> "BaseLLM":
        """LLM 인스턴스를 비동기적으로 생성하고 MCP 서버에 자동으로 연결합니다.

        Args:
            model: LLM 모델 이름
            **kwargs: LLM 생성자 인자
                - mcp_servers: MCP 서버 설정 리스트
                - 기타 LLM 관련 설정

        Returns:
            MCP가 초기화된 LLM 인스턴스

        Examples:
            # 단일 MCP 서버
            llm = await LLM.create_async(
                "gpt-4o-mini",
                mcp_servers=McpConfig(
                    name="calculator",
                    cmd="python calculator.py"
                )
            )

            # 여러 MCP 서버
            llm = await LLM.create_async(
                "gpt-4o-mini",
                mcp_servers=[
                    McpConfig(name="calc", cmd="..."),
                    McpConfig(name="web", url="...")
                ]
            )
        """
        # 동기 create 메서드로 LLM 인스턴스 생성
        llm = cls.create(model, **kwargs)

        # MCP 서버가 설정되어 있으면 자동으로 연결
        if hasattr(llm, "mcp_servers") and llm.mcp_servers:
            await llm.initialize_mcp()

        return llm

    @classmethod
    def get_price(cls, model: Union[LLMChatModelType, LLMEmbeddingModelType], usage: Usage) -> Price:
        try:
            input_per_1m, output_per_1m = cls.MODEL_PRICES[model]
        except KeyError:
            return Price()

        if input_per_1m:
            input_per_1m = Decimal(input_per_1m)
            input_usd = (Decimal(usage.input) * input_per_1m) / Decimal("1_000_000")
        else:
            input_usd = None

        if output_per_1m:
            output_per_1m = Decimal(output_per_1m)
            output_usd = (Decimal(usage.input) * output_per_1m) / Decimal("1_000_000")
        else:
            output_usd = None

        return Price(input_usd=input_usd, output_usd=output_usd)


def __getattr__(name):
    """Lazy import provider classes to avoid import errors when optional dependencies are not installed."""
    if name == "AnthropicLLM":
        from pyhub.llm.anthropic import AnthropicLLM

        return AnthropicLLM
    elif name == "GoogleLLM":
        from pyhub.llm.google import GoogleLLM

        return GoogleLLM
    elif name == "OllamaLLM":
        from pyhub.llm.ollama import OllamaLLM

        return OllamaLLM
    elif name == "OpenAILLM":
        from pyhub.llm.openai import OpenAILLM

        return OpenAILLM
    elif name == "UpstageLLM":
        from pyhub.llm.upstage import UpstageLLM

        return UpstageLLM
    elif name == "hub":
        import pyhub.llm.hub as _hub

        return _hub
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "LLM",
    "BaseLLM",
    "SequentialChain",
    "display",
    "print_stream",
    "AnthropicLLM",
    "GoogleLLM",
    "MockLLM",
    "OllamaLLM",
    "OpenAILLM",
    "UpstageLLM",
    "hub",
]
