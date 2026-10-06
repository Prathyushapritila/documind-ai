import unittest

from document_search import search_document


class DocumentSearchTests(unittest.TestCase):
    def test_finds_total_amount_with_page_source(self):
        pages = [
            {
                "page_number": 1,
                "text": "Vendor: Bright Office Supplies",
            },
            {
                "page_number": 2,
                "text": "Total Amount: $540.00",
            },
        ]

        result = search_document(pages, "What is the total amount?")

        self.assertEqual(result["answer"], "Total Amount: $540.00")
        self.assertEqual(result["source"], "Page 2")
        self.assertEqual(result["status"], "found")

    def test_unsupported_question_returns_not_found(self):
        pages = [
            {
                "page_number": 1,
                "text": "Total Amount: $540.00",
            }
        ]

        result = search_document(pages, "What color is the product?")

        self.assertEqual(result["answer"], "Not found in the document.")
        self.assertEqual(result["status"], "not_found")
        self.assertEqual(result["source"], "—")

    def test_empty_question_returns_not_found(self):
        result = search_document([], "   ")

        self.assertEqual(result["answer"], "Not found in the document.")
        self.assertEqual(result["status"], "not_found")

    def test_evidence_length_is_limited(self):
        pages = [
            {
                "page_number": 1,
                "text": "Vendor: " + ("A" * 600),
            }
        ]

        result = search_document(pages, "Who is the vendor?")

        self.assertEqual(len(result["evidence"]), 500)
        self.assertEqual(result["source"], "Page 1")


if __name__ == "__main__":
    unittest.main()