# Agent Guide for this RAG Project

This document provides essential information for agents working with this Retrieval-Augmented Generation (RAG) project that ingests PDF content and allows querying via CLI.

## Project Overview

This is a Python-based RAG application that:
- Ingests PDF documents into a PostgreSQL database with pgvector embeddings
- Allows users to ask questions via CLI about the document content
- Uses either OpenAI or Google AI providers for embeddings and language models
- Enforces strict context boundaries - responses are only based on document content

## Project Structure

```
.
├── README.md           # Project documentation
├── docker-compose.yml  # Docker setup for PostgreSQL with pgvector
├── requirements.txt    # Python dependencies
├── src/
│   ├── chat.py         # CLI chat interface
│   ├── config.py       # Configuration and environment loading
│   ├── ingest.py       # PDF ingestion logic
│   ├── providers.py    # AI provider selection (OpenAI/Google)
│   └── search.py       # Vector search and prompt building
├── document.pdf        # Default PDF to process (can be overridden with PDF_PATH)
└── .env.example        # Environment variable examples
```

## Essential Commands

### Setup and Installation
```bash
# Start PostgreSQL database
docker compose up -d

# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment variables (see .env.example)
```

### Usage
```bash
# Ingest PDF content into vector database
python src/ingest.py

# Start CLI chat interface
python src/chat.py
```

## Configuration

The application uses environment variables for configuration:

Required variables:
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+psycopg://postgres:postgres@localhost:5432/rag`)
- `EMBEDDINGS_PROVIDER`: Either `openai` or `gemini`
- `LLM_PROVIDER`: Either `openai` or `gemini`

Provider-specific API keys:
- `OPENAI_API_KEY` (when provider is `openai`)
- `GOOGLE_API_KEY` (when provider is `gemini`)

Optional variables:
- `PDF_PATH`: Path to PDF file (default: `document.pdf`)

## Code Patterns and Conventions

### Key Components
1. **Configuration Management** (`config.py`): Uses dataclass for settings with validation
2. **Provider Selection** (`providers.py`): Factory functions that return appropriate embedding and LLM clients based on configuration
3. **Ingestion Pipeline** (`ingest.py`): PDF loading → text splitting → vector storage
4. **Search Logic** (`search.py`): Vector similarity search with context formatting
5. **Prompt Engineering** (`search.py`): Strict prompt template enforcing context boundaries

### Key Constants
- `CHUNK_SIZE = 1000`, `CHUNK_OVERLAP = 150`: Text splitting parameters
- `TOP_K = 10`: Number of similar chunks to retrieve for each query
- `COLLECTION_NAME = "document_chunks"`: Vector store collection name

### Model Versions (in `providers.py`)
- OpenAI: `gpt-5-nano` (LLM), `text-embedding-3-small` (embeddings)
- Gemini: `gemini-2.5-flash-lite` (LLM), `models/embedding-001` (embeddings)
- All LLMs use `temperature=0` for deterministic responses

### Language Convention
- All user-facing output is in Portuguese (e.g., prompts, CLI messages, error messages)
- Keep this consistent when modifying any print statements or prompt templates

### Error Handling
- Environment validation with descriptive error messages
- Graceful handling of missing files and invalid configurations
- Exception handling in main execution flows

## Testing Approach

This project is primarily functional and doesn't appear to have explicit tests. The main testing approach would be:
1. Manual testing of the ingestion pipeline 
2. Manual testing of chat functionality
3. Verifying database connections and vector operations

## Important Gotchas

1. **Database Setup**: PostgreSQL with pgvector must be running before ingestion or chat
2. **API Keys**: Must provide correct API keys for chosen providers (OpenAI or Google)
3. **Context Boundaries**: The system strictly enforces that responses are only based on document content - it will return a predefined message if information isn't in context
4. **PDF Content**: The ingestion process splits text into chunks, so very long documents might be truncated during processing
5. **Environment Variables**: Must be properly configured before running either ingest or chat commands

## Implementation Details

### Ingestion Process
1. Load PDF using `PyPDFLoader`
2. Split content into chunks with `RecursiveCharacterTextSplitter`
3. Store chunks in PostgreSQL with pgvector embeddings
4. Each chunk gets metadata including source and chunk index

### Chat Interface
1. Uses vector search to find relevant document chunks
2. Builds a prompt that includes the retrieved context
3. Sends the prompt to the configured LLM
4. Returns only the LLM's response (no additional processing)

## Deployment Considerations

- Requires Docker for PostgreSQL setup
- Needs API keys for either OpenAI or Google AI services
- Uses Python virtual environment for dependency isolation
- Assumes PostgreSQL with pgvector extension is available