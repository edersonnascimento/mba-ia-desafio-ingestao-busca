from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import Settings

EMBEDDINGS_MODEL_OPENAI = "text-embedding-3-small"
EMBEDDINGS_MODEL_GEMINI = "models/embedding-001"
LLM_MODEL_OPENAI = "gpt-5-nano"
LLM_MODEL_GEMINI = "gemini-2.5-flash-lite"


def get_embeddings(settings: Settings):
    """Return the configured embeddings client based on settings."""

    if settings.embeddings_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when EMBEDDINGS_PROVIDER=openai."
            )
        return OpenAIEmbeddings(
            model=EMBEDDINGS_MODEL_OPENAI, api_key=settings.openai_api_key
        )

    if not settings.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required when EMBEDDINGS_PROVIDER=gemini."
        )
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDINGS_MODEL_GEMINI, google_api_key=settings.google_api_key
    )


def get_llm(settings: Settings):
    """Return the configured chat model based on settings."""

    if not settings.llm_provider:
        raise ValueError("LLM_PROVIDER is required.")

    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )
        return ChatOpenAI(
            model=LLM_MODEL_OPENAI, api_key=settings.openai_api_key, temperature=0
        )

    if not settings.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required when LLM_PROVIDER=gemini."
        )
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL_GEMINI, google_api_key=settings.google_api_key, temperature=0
    )
