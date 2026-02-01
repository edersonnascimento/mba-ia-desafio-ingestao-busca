# Desafio MBA Engenharia de Software com IA - Full Cycle

## Visao geral
Este projeto ingere um PDF, grava embeddings no PostgreSQL com pgvector e
permite perguntas via CLI com respostas baseadas apenas no conteudo do PDF.

## Requisitos
- Python 3.11+
- Docker e Docker Compose

## Configuracao
1) Suba o Postgres com pgvector:
```
docker compose up -d
```

2) Instale as dependencias:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Configure as variaveis de ambiente (exemplo):
```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
EMBEDDINGS_PROVIDER=openai
LLM_PROVIDER=openai
OPENAI_API_KEY=...
```

Variaveis obrigatorias:
- `DATABASE_URL`: string de conexao `postgresql+psycopg://...`
- `EMBEDDINGS_PROVIDER`: `openai` ou `gemini`
- `LLM_PROVIDER`: `openai` ou `gemini`
- `OPENAI_API_KEY` quando provider for `openai`
- `GOOGLE_API_KEY` quando provider for `gemini`

Opcional:
- `PDF_PATH`: caminho para o PDF (padrao: `document.pdf`)

## Ingestao
Execute a ingestao do PDF:
```
python src/ingest.py
```

## Chat
Inicie o CLI de perguntas:
```
python src/chat.py
```

Saida fora do contexto deve ser sempre:
```
Nao tenho informacoes necessarias para responder sua pergunta.
```