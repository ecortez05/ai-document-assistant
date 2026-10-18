import io

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .chunking import split_text


def extract_chunks(data: bytes) -> tuple[int, list[tuple[int, str]]]:
    """Return (page_count, [(page_number, chunk_text), ...])."""
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = [p.extract_text() or "" for p in reader.pages]
    except PdfReadError:
        raise ValueError("Could not read that file as a PDF")

    out = []
    for number, text in enumerate(pages, start=1):
        for piece in split_text(text):
            out.append((number, piece))
    return len(pages), out
