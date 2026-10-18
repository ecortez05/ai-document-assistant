import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/docassist"
)
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 5
MAX_UPLOAD_MB = 20
