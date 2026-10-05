import unittest

import pymupdf

from pdf_inspection import MAX_PAGE_COUNT, inspect_pdf


def create_test_pdf(
    text: str = "",
    page_count: int = 1,
    password: str | None = None,
) -> bytes:
    """Create a temporary PDF entirely in memory."""

    document = pymupdf.open()

    for page_index in range(page_count):
        page = document.new_page()

        if text and page_index == 0:
            page.insert_text((72, 72), text)

    if password:
        pdf_bytes = document.tobytes(
            encryption=pymupdf.PDF_ENCRYPT_AES_256,
            owner_pw="owner-password",
            user_pw=password,
        )
    else:
        pdf_bytes = document.tobytes()

    document.close()
    return pdf_bytes


class PdfInspectionTests(unittest.TestCase):
    def test_valid_pdf_is_read(self):
        pdf_bytes = create_test_pdf("Vendor: Bright Office Supplies")

        result, error = inspect_pdf(pdf_bytes)

        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertEqual(result["page_count"], 1)
        self.assertIn("Vendor: Bright Office Supplies", result["text"])
        self.assertEqual(result["pages"][0]["page_number"], 1)

    def test_fake_pdf_is_rejected(self):
        result, error = inspect_pdf(b"This is not really a PDF.")

        self.assertIsNone(result)
        self.assertEqual(
            error,
            "The uploaded file is not a valid PDF.",
        )

    def test_blank_pdf_is_rejected(self):
        pdf_bytes = create_test_pdf()

        result, error = inspect_pdf(pdf_bytes)

        self.assertIsNone(result)
        self.assertIn("No readable text was found", error)

    def test_too_many_pages_are_rejected(self):
        pdf_bytes = create_test_pdf(
            text="Test document",
            page_count=MAX_PAGE_COUNT + 1,
        )

        result, error = inspect_pdf(pdf_bytes)

        self.assertIsNone(result)
        self.assertIn("The limit is 50 pages", error)

    def test_password_protected_pdf_is_rejected(self):
        pdf_bytes = create_test_pdf(
            text="Private information",
            password="secret-password",
        )

        result, error = inspect_pdf(pdf_bytes)

        self.assertIsNone(result)
        self.assertEqual(
            error,
            "Password-protected PDFs are not supported.",
        )


if __name__ == "__main__":
    unittest.main()