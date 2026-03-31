# Desafio MBA Engenharia de Software com IA - Full Cycle

## Visão geral
Este projeto ingere um PDF, grava embeddings no PostgreSQL com pgvector e
permite perguntas via CLI com respostas baseadas apenas no conteúdo do PDF.

## Requisitos
- Python 3.11+
- Docker e Docker Compose

## Configuração

### 1. Inicie o PGVector
```bash
docker compose up -d
```

Para parar o banco de dados:
```bash
docker compose stop
```

Para interromper e remover os containers:
```bash
docker compose down
```

> Com o flag `-v` os dados são apagados junto com os containers:
> ```bash
> docker compose down -v
> ```

### 2. Instale as dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Copie o exemplo e edite com suas chaves:
```bash
cp .env.example .env
```

Exemplo de `.env` com OpenAI:
```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
EMBEDDINGS_PROVIDER=openai
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
```

Exemplo de `.env` com Gemini:
```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
EMBEDDINGS_PROVIDER=gemini
LLM_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_aqui
```

É possível combinar providers (ex: embeddings com OpenAI e LLM com Gemini).

### 4. Colocar o PDF
Certifique-se de que o arquivo `document.pdf` existe na raiz do projeto,
ou defina `PDF_PATH` no `.env` para apontar para outro arquivo.

## Ingestão
Execute a ingestão do PDF:
```bash
python3 src/ingest.py
```

> **Atenção:** rodar a ingestão múltiplas vezes sobrescreve os chunks existentes
> (usamos ids determinísticos). Não há duplicação, mas o processo re-calcula
> todos os embeddings.

## Chat
Inicie o CLI de perguntas:
```bash
python3 src/chat.py
```

Resposta quando a pergunta está fora do contexto:
```
Não tenho informações necessárias para responder sua pergunta.
```