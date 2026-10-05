from pathlib import Path

import fitz


OUTPUT_DIRECTORY = Path("sample_documents")
OUTPUT_FILE = OUTPUT_DIRECTORY / "sample_invoice.pdf"

OUTPUT_DIRECTORY.mkdir(exist_ok=True)

document = fitz.open()
page = document.new_page()

sample_invoice = """
SAMPLE INVOICE — NOT A REAL TRANSACTION

Vendor: Bright Office Supplies
Customer: Example Design Studio
Invoice Number: INV-2026-1042
Invoice Date: October 4, 2026
Due Date: October 19, 2026

Description: Ergonomic office chairs
Quantity: 2
Price per item: $250.00

Subtotal: $500.00
Tax: $40.00
Total Amount: $540.00

Payment Terms: Payment is due within 15 days.
Contact: billing@example.invalid
"""

page.insert_text(
    (72, 72),
    sample_invoice,
    fontsize=12,
    fontname="helv",
)

document.set_metadata(
    {
        "title": "Synthetic Sample Invoice",
        "author": "DocuMind AI Project",
        "subject": "Testing only",
    }
)

document.save(OUTPUT_FILE)
document.close()

print(f"Created safe sample PDF: {OUTPUT_FILE}")