import re


INVOICE_FIELDS = [
    "Vendor",
    "Customer",
    "Invoice Number",
    "Invoice Date",
    "Due Date",
    "Subtotal",
    "Tax",
    "Total Amount",
    "Payment Terms",
]

INVOICE_FIELD_LABELS = {
    "Vendor": ["Vendor", "Seller", "Supplier"],
    "Customer": ["Customer", "Bill To", "Billed To"],
    "Invoice Number": ["Invoice Number", "Invoice No", "Invoice #"],
    "Invoice Date": ["Invoice Date", "Date Issued", "Issue Date"],
    "Due Date": ["Due Date", "Payment Due", "Pay By"],
    "Subtotal": ["Subtotal", "Sub Total"],
    "Tax": ["Tax", "Sales Tax", "VAT"],
    "Total Amount": [
        "Total Amount",
        "Grand Total",
        "Amount Due",
        "Balance Due",
    ],
    "Payment Terms": ["Payment Terms", "Terms"],
}
def clean_extracted_value(value: str) -> str:
    """Clean whitespace and limit the displayed value length."""

    cleaned_value = " ".join(value.split())
    return cleaned_value[:200]


def find_labeled_field(pages: list[dict], label: str) -> dict:
    """Extract an exactly labeled field without guessing."""

    pattern = re.compile(
        rf"(?im)^\s*{re.escape(label)}\s*:\s*(.+?)\s*$"
    )

    for page_information in pages:
        match = pattern.search(page_information["text"])

        if match:
            return {
                "Field": label,
                "Value": clean_extracted_value(match.group(1)),
                "Source": f"Page {page_information['page_number']}",
                "Method": "Exact label",
            }

    return {
        "Field": label,
        "Value": "Not found",
        "Source": "—",
        "Method": "Not guessed",
    }


def extract_invoice_fields(pages: list[dict]) -> list[dict]:
    """Extract approved invoice fields and label aliases."""

    results = []

    for field in INVOICE_FIELDS:
        result = find_labeled_field(pages, field)

        if result["Value"] == "Not found":
            for alias in INVOICE_FIELD_LABELS[field][1:]:
                alias_result = find_labeled_field(pages, alias)

                if alias_result["Value"] != "Not found":
                    alias_result["Field"] = field
                    alias_result["Method"] = "Approved alias"
                    result = alias_result
                    break

        results.append(result)

    return results