import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import load_settings
from providers import get_embeddings

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
COLLECTION_NAME = "document_chunks"


def ingest_pdf() -> None:
    """Ingest the configured PDF into PGVector."""

    settings = load_settings(require_pdf=True)
    embeddings = get_embeddings(settings)

    loader = PyPDFLoader(settings.pdf_path)
    documents = loader.load()
    if not documents:
        raise ValueError("PDF loaded no content to ingest.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("Text splitter produced no chunks to ingest.")

    source_name = os.path.basename(settings.pdf_path)
    ids: list[str] = []
    for index, chunk in enumerate(chunks):
        chunk.metadata = {
            **chunk.metadata,
            "chunk_index": index,
            "source": source_name,
        }
        ids.append(f"{source_name}:{index}")

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=settings.database_url,
        use_jsonb=True,
    )
    vector_store.add_documents(chunks, ids=ids)

    print(f"Ingestao concluida. Chunks inseridos: {len(chunks)}")


if __name__ == "__main__":
    try:
        ingest_pdf()
    except Exception as exc:
        print(f"Erro na ingestao: {exc}")