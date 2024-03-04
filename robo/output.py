import csv
import io

from robo.extractor import Result


def to_csv(results: list[Result]) -> str:
    """Convert a list of `Result` objects (which are essentially Python
    dictionaries) into a CSV string."""
    csv_string: str = ""
    if results:
        # Jump through some hoops to write to a string in memory rather than a
        # file, for easier testing and more flexibility overall.
        output = io.StringIO()
        field_names = results[0].keys()
        writer = csv.DictWriter(output, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(results)
        csv_string = output.getvalue()
    return csv_string
