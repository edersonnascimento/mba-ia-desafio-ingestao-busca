from langchain_postgres import PGVector

from config import Settings, load_settings
from providers import get_embeddings

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 10
COLLECTION_NAME = "document_chunks"
OUT_OF_CONTEXT_ANSWER = (
    "Nao tenho informacoes necessarias para responder sua pergunta."
)

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informacao nao estiver explicitamente no CONTEXTO, responda:
  "{out_of_context_answer}"
- Nunca invente ou use conhecimento externo.
- Nunca produza opinioes ou interpretacoes alem do que esta escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual e a capital da Franca?"
Resposta: "{out_of_context_answer}"

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "{out_of_context_answer}"

Pergunta: "Voce acha isso bom ou ruim?"
Resposta: "{out_of_context_answer}"

PERGUNTA DO USUARIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUARIO"
"""


def search_context(
    question: str,
    *,
    settings: Settings | None = None,
    return_scores: bool = False,
) -> tuple[str, list[tuple[object, float]]]:
    """Retrieve context for a question from the vector store."""

    if not question or not question.strip():
        raise ValueError("Pergunta vazia.")

    settings = settings or load_settings()
    embeddings = get_embeddings(settings)

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=settings.database_url,
        use_jsonb=True,
    )
    results = vector_store.similarity_search_with_score(
        query=question, k=TOP_K
    )
    context = "\n\n---\n\n".join(
        doc.page_content for doc, _score in results
    ).strip()

    if return_scores:
        return context, results
    return context, []


def build_prompt(context: str, question: str) -> str:
    """Build the final LLM prompt with context and user question."""

    return PROMPT_TEMPLATE.format(
        contexto=context,
        pergunta=question,
        out_of_context_answer=OUT_OF_CONTEXT_ANSWER,
    )


def search_prompt(question: str) -> str:
    """Generate a full prompt for the given question."""

    context, _ = search_context(question)
    return build_prompt(context, question)