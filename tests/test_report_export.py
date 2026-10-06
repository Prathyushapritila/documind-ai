import csv
import io
import unittest

from report_export import build_csv_report, make_safe_csv_value


class ReportExportTests(unittest.TestCase):
    def test_report_contains_expected_columns_and_values(self):
        extracted_fields = [
            {
                "Field": "Total Amount",
                "Value": "$540.00",
                "Source": "Page 1",
                "Method": "Exact label",
            }
        ]

        report = build_csv_report(extracted_fields)
        rows = list(csv.DictReader(io.StringIO(report)))

        self.assertEqual(
            list(rows[0].keys()),
            ["Field", "Value", "Source", "Method"],
        )
        self.assertEqual(rows[0]["Value"], "$540.00")
        self.assertEqual(rows[0]["Source"], "Page 1")

    def test_missing_values_become_empty_cells(self):
        report = build_csv_report([{"Field": "Vendor"}])
        rows = list(csv.DictReader(io.StringIO(report)))

        self.assertEqual(rows[0]["Field"], "Vendor")
        self.assertEqual(rows[0]["Value"], "")
        self.assertEqual(rows[0]["Source"], "")
        self.assertEqual(rows[0]["Method"], "")

    def test_spreadsheet_formula_prefixes_are_neutralized(self):
        for unsafe_value in ["=1+1", "+SUM(A1:A2)", "-10+20", "@command"]:
            with self.subTest(unsafe_value=unsafe_value):
                safe_value = make_safe_csv_value(unsafe_value)
                self.assertTrue(safe_value.startswith("'"))

    def test_unapproved_extra_data_is_not_exported(self):
        extracted_fields = [
            {
                "Field": "Vendor",
                "Value": "Example Company",
                "Source": "Page 1",
                "Method": "Exact label",
                "PrivateDocumentText": "Do not export this",
            }
        ]

        report = build_csv_report(extracted_fields)

        self.assertNotIn("PrivateDocumentText", report)
        self.assertNotIn("Do not export this", report)


if __name__ == "__main__":
    unittest.main()