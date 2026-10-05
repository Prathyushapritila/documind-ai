import fitz
import streamlit as st

MAX_FILE_SIZE_MB = 10
MAX_PAGE_COUNT = 50
MAX_PREVIEW_CHARACTERS = 5_000


def inspect_pdf(pdf_bytes: bytes):
    """Safely inspect a PDF and extract readable text."""

    if not pdf_bytes.startswith(b"%PDF-"):
        return None, "The uploaded file is not a valid PDF."

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            if document.needs_pass:
                return None, "Password-protected PDFs are not supported."

            if document.page_count == 0:
                return None, "The PDF does not contain any pages."

            if document.page_count > MAX_PAGE_COUNT:
                return None, (
                    f"The PDF contains {document.page_count} pages. "
                    f"The current safety limit is {MAX_PAGE_COUNT} pages."
                )

            page_texts = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    page_texts.append(
                        f"--- Page {page_number} ---\n{text}"
                    )

            complete_text = "\n\n".join(page_texts)

            result = {
                "page_count": document.page_count,
                "character_count": len(complete_text),
                "text": complete_text,
            }

    except Exception:
        return None, (
            "DocuMind could not safely read this PDF. "
            "The file may be damaged or use an unsupported format."
        )

    if not result["text"]:
        return None, (
            "No readable text was found. This may be a scanned document. "
            "Image-based OCR will be added in a later version."
        )

    return result, None


st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
)

st.title("📄 DocuMind AI")
st.write(
    "A privacy-first document assistant for freelancers "
    "and small businesses."
)

st.info(
    "Guardrail: DocuMind explains information found in a document. "
    "It does not provide legal, medical, tax, or financial advice."
)

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="Only PDF files up to 10 MB are accepted.",
)

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error("The file is too large. Upload a PDF up to 10 MB.")

    else:
        pdf_bytes = uploaded_file.getvalue()
        result, error = inspect_pdf(pdf_bytes)

        if error:
            st.error(error)

        else:
            st.success("The PDF was read successfully.")

            column_one, column_two, column_three = st.columns(3)

            column_one.metric("Pages", result["page_count"])
            column_two.metric(
                "Characters",
                f"{result['character_count']:,}",
            )
            column_three.metric(
                "Size",
                f"{file_size_mb:.2f} MB",
            )

            st.subheader("Extracted text preview")

            preview = result["text"][:MAX_PREVIEW_CHARACTERS]

            st.text_area(
                "Document text",
                value=preview,
                height=350,
                disabled=True,
            )

            if len(result["text"]) > MAX_PREVIEW_CHARACTERS:
                st.caption(
                    "Only the first 5,000 characters are displayed "
                    "to keep the preview manageable."
                )

            st.warning(
                "This version processes the file temporarily in memory. "
                "Continue using only public or sample documents."
            )