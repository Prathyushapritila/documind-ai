from document_search import search_document

from invoice_extraction import (
    extract_invoice_fields,
)
from pdf_inspection import inspect_pdf



import streamlit as st


MAX_FILE_SIZE_MB = 10
MAX_PREVIEW_CHARACTERS = 5_000







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

            st.subheader("Invoice field extraction")

            st.caption(
                "Guardrail: Only exactly labeled fields are extracted. "
                "Missing information is reported as “Not found.”"
            )

            extracted_fields = extract_invoice_fields(result["pages"])
            

            st.dataframe(
                extracted_fields,
                width="stretch",
                hide_index=True,
            )
            st.subheader("Ask this document")

            st.caption(
                "Answers use only matching evidence from the uploaded document. "
                "Unsupported answers are reported as “Not found in the document.”"
            )

            question = st.text_input(
                "Your question",
                placeholder="What is the total amount?",
            )

            if question:
                search_result = search_document(result["pages"], question)

                if search_result["status"] == "found":
                    st.success(search_result["answer"])
                    st.caption(
                        f"Source: {search_result['source']} · "
                        f"Method: {search_result['method']}"
                    )

                    with st.expander("View supporting evidence"):
                        st.write(search_result["evidence"])
                else:
                    st.warning("Not found in the document.")
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
                    "Only the first 5,000 characters are displayed."
                )

            st.warning(
                "This version processes the file temporarily in memory. "
                "Continue using only public or sample documents."
            )