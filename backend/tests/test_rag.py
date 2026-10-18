from app.services.rag import build_prompt


def test_prompt_numbers_excerpts_and_ends_with_question():
    prompt = build_prompt(
        "What is the refund policy?",
        [("terms.pdf", 3, "Refunds within 30 days."), ("faq.pdf", 1, "Contact support.")],
    )
    assert "[1] (terms.pdf, page 3)" in prompt
    assert "[2] (faq.pdf, page 1)" in prompt
    assert prompt.rstrip().endswith("Question: What is the refund policy?")
