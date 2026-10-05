import pymupdf


MAX_PAGE_COUNT = 50


def inspect_pdf(pdf_bytes: bytes):
    """Safely inspect a PDF and extract readable text."""

    if not pdf_bytes.startswith(b"%PDF-"):
        return None, "The uploaded file is not a valid PDF."

    try:
        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf",
        ) as document:
            if document.needs_pass:
                return None, "Password-protected PDFs are not supported."

            if document.page_count == 0:
                return None, "The PDF does not contain any pages."

            if document.page_count > MAX_PAGE_COUNT:
                return None, (
                    f"The PDF has {document.page_count} pages. "
                    f"The limit is {MAX_PAGE_COUNT} pages."
                )

            pages = []

            for page_number, page in enumerate(document, start=1):
                page_text = page.get_text("text").strip()

                pages.append(
                    {
                        "page_number": page_number,
                        "text": page_text,
                    }
                )

            readable_pages = [
                page_information
                for page_information in pages
                if page_information["text"]
            ]

            if not readable_pages:
                return None, (
                    "No readable text was found. "
                    "This may be a scanned document."
                )

            full_text = "\n\n".join(
                (
                    f"--- Page {page_information['page_number']} ---\n"
                    f"{page_information['text']}"
                )
                for page_information in pages
            )

            return {
                "pages": pages,
                "text": full_text,
                "page_count": document.page_count,
                "character_count": len(full_text),
            }, None

    except (pymupdf.FileDataError, RuntimeError, ValueError):
        return None, "The PDF could not be opened safely."