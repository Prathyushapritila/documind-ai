import re


MAX_QUESTION_LENGTH = 300
MAX_EVIDENCE_LENGTH = 500

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "document",
    "for",
    "from",
    "in",
    "invoice",
    "is",
    "it",
    "me",
    "of",
    "on",
    "please",
    "show",
    "tell",
    "the",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "with",
}


def tokenize(text: str) -> set[str]:
    """Convert text into useful lowercase search words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word
        for word in words
        if len(word) > 1 and word not in STOP_WORDS
    }


def not_found_result() -> dict:
    """Return a safe response when supporting evidence is unavailable."""
    return {
        "answer": "Not found in the document.",
        "evidence": "",
        "source": "—",
        "method": "No evidence match",
        "status": "not_found",
    }


def search_document(pages: list[dict], question: str) -> dict:
    """Find the document line that best supports the question."""
    safe_question = " ".join(question.split())[:MAX_QUESTION_LENGTH]
    question_words = tokenize(safe_question)

    if not question_words:
        return not_found_result()

    best_score = 0
    best_line = ""
    best_page_number = None

    for page in pages:
        for line in page["text"].splitlines():
            clean_line = " ".join(line.split())

            if not clean_line:
                continue

            matching_words = question_words & tokenize(clean_line)
            score = len(matching_words)

            if score > best_score:
                best_score = score
                best_line = clean_line[:MAX_EVIDENCE_LENGTH]
                best_page_number = page["page_number"]

    if best_score == 0:
        return not_found_result()

    return {
        "answer": best_line,
        "evidence": best_line,
        "source": f"Page {best_page_number}",
        "method": "Keyword evidence match",
        "status": "found",
    }