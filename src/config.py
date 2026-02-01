import os
from dataclasses import dataclass

from dotenv import load_dotenv

SUPPORTED_PROVIDERS = ("openai", "gemini")
DEFAULT_PDF_PATH = "document.pdf"


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    database_url: str
    embeddings_provider: str
    llm_provider: str | None
    openai_api_key: str | None
    google_api_key: str | None
    pdf_path: str


def _normalize_provider(value: str | None, name: str) -> str:
    if not value or not value.strip():
        raise ValueError(f"{name} is required.")
    provider = value.strip().lower()
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"{name} must be one of {', '.join(SUPPORTED_PROVIDERS)}."
        )
    return provider


def load_settings(
    *, require_llm: bool = False, require_pdf: bool = False
) -> Settings:
    """Load and validate environment settings for the current script."""

    load_dotenv()

    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise ValueError("DATABASE_URL is required.")

    embeddings_provider = _normalize_provider(
        os.getenv("EMBEDDINGS_PROVIDER"), "EMBEDDINGS_PROVIDER"
    )

    llm_provider = None
    llm_env = os.getenv("LLM_PROVIDER")
    if require_llm or llm_env:
        llm_provider = _normalize_provider(llm_env, "LLM_PROVIDER")

    pdf_path = os.getenv("PDF_PATH", DEFAULT_PDF_PATH).strip() or DEFAULT_PDF_PATH
    if require_pdf and not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at '{pdf_path}'.")

    return Settings(
        database_url=database_url,
        embeddings_provider=embeddings_provider,
        llm_provider=llm_provider,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        pdf_path=pdf_path,
    )
