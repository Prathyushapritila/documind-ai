import csv
import io


REPORT_COLUMNS = ["Field", "Value", "Source", "Method"]
UNSAFE_SPREADSHEET_PREFIXES = ("=", "+", "-", "@")


def make_safe_csv_value(value: object) -> str:
    """Convert a value to text and prevent spreadsheet formula execution."""
    text = str(value)

    if text.lstrip().startswith(UNSAFE_SPREADSHEET_PREFIXES):
        return "'" + text

    return text


def build_csv_report(extracted_fields: list[dict]) -> str:
    """Create a CSV report containing only verified extraction results."""
    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=REPORT_COLUMNS,
        extrasaction="ignore",
        lineterminator="\n",
    )
    writer.writeheader()

    for extracted_field in extracted_fields:
        safe_row = {
            column: make_safe_csv_value(extracted_field.get(column, ""))
            for column in REPORT_COLUMNS
        }
        writer.writerow(safe_row)

    return output.getvalue()