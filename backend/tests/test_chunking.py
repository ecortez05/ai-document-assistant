from app.services.chunking import split_text


def test_empty_text():
    assert split_text("   \n ") == []


def test_short_text_is_one_chunk():
    assert split_text("Just a short note.") == ["Just a short note."]


def test_long_text_overlaps():
    text = " ".join(f"word{i}" for i in range(600))
    chunks = split_text(text, size=300, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)
    # the tail of one chunk should show up at the start of the next
    tail = chunks[0].split()[-2:]
    assert all(w in chunks[1] for w in tail)


def test_nothing_is_lost():
    text = " ".join(f"w{i}" for i in range(400))
    joined = " ".join(split_text(text, size=200, overlap=0))
    assert joined.split() == text.split()
