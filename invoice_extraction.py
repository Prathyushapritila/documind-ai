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
    """Extract the approved invoice fields from document pages."""

    return [
        find_labeled_field(pages, field)
        for field in INVOICE_FIELDS
    ]