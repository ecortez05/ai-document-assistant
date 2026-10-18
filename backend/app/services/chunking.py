from ..config import CHUNK_OVERLAP, CHUNK_SIZE


def split_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping pieces, trying to end on a sentence or space."""
    text = " ".join(text.split())
    if not text:
        return []

    pieces = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = max(text.rfind(". ", start, end), text.rfind(" ", start, end))
            if cut > start + size // 2:
                end = cut + 1
        pieces.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - overlap
    return pieces
