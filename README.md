# AI Document Assistant

Upload PDFs and ask questions about them in plain English. Answers come back with the pages they were pulled from, so you can check them.

It's a retrieval-augmented generation (RAG) app: PDFs are split into chunks, each chunk gets a vector embedding stored in PostgreSQL (pgvector), and a question is answered from the closest chunks.

**Stack:** Python, FastAPI, React, PostgreSQL + pgvector, OpenAI API, Docker, GitHub Actions, AWS

## How it works

1. **Upload** – `pypdf` pulls text out of each page, which is split into ~900 character overlapping chunks.
2. **Embed** – chunks are embedded with `text-embedding-3-small` and saved in a `vector(1536)` column.
3. **Ask** – the question is embedded, the 5 nearest chunks (cosine distance) are fetched from the user's own documents, and passed to the chat model with instructions to answer only from them.
4. **Cite** – the response includes the filename, page, and snippet for each chunk used.

Auth is email + password (bcrypt) with JWT bearer tokens. Every query is scoped to the logged-in user's documents.

## Running it

You need Docker and an OpenAI API key.

```bash
cp .env.example .env     # add your OPENAI_API_KEY
docker compose up --build
```

- App: http://localhost:3000
- API docs: http://localhost:8000/docs

### Without Docker

```bash
# postgres with pgvector needs to be running, then:
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/docassist
export OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload

cd ../frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
python -m pytest
```

Covers auth (register/login/token checks), the text chunker, and prompt building. OpenAI is never called in tests.

## CI/CD

`.github/workflows/ci.yml` runs the backend tests and a frontend build on every push and PR. On `main` it builds the Docker images, pushes them to Amazon ECR, and restarts the stack on an EC2 instance over SSH.

Secrets needed: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `EC2_HOST`, `EC2_SSH_KEY`.

## API

| Method | Path | Description |
| --- | --- | --- |
| POST | `/auth/register` | create account, returns token |
| POST | `/auth/login` | returns token |
| GET | `/documents` | list your documents |
| POST | `/documents` | upload a PDF |
| DELETE | `/documents/{id}` | delete a document and its chunks |
| POST | `/chat` | `{question, document_id?}` → answer + sources |

## Limitations

- Scanned PDFs without a text layer aren't supported (no OCR).
- Tables and multi-column layouts can come out jumbled from `pypdf`.
- Embedding happens inside the upload request, so large files take a while.
