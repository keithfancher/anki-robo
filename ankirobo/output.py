import csv
import io
import json

from ankirobo.types import Result


def to_csv(results: list[Result], extractor_name: str) -> str:
    """Convert a list of `Result` objects (which are essentially Python
    dictionaries) into a CSV string, including some useful Anki metadata."""
    csv_string: str = ""
    if results:
        # Jump through some hoops to write to a string in memory rather than a
        # file, for easier testing and more flexibility overall.
        output = io.StringIO()
        # First, manually write the Anki CSV header:
        sample_result = results[0]
        output.write(anki_csv_header(extractor_name))
        # Then initialize the csv writer, which does the hard work for us:
        csvwriter = csv.DictWriter(output, fieldnames=sample_result.keys())
        # Note that this is actually written as part of the Anki CSV header above:
        csvwriter.writeheader()
        # ...and THEN we write the rows-proper:
        csvwriter.writerows(results)
        csv_string = output.getvalue()
        output.close()
    return csv_string


def anki_csv_header(extractor_name: str) -> str:
    """Anki-specific CSV header data. See:
    https://docs.ankiweb.net/importing/text-files.html#file-headers"""
    return "\n".join(
        [
            "#separator:Comma",
            f"#tags:AnkiRobo {extractor_name}",
            "#deck:AnkiRobo",
            "#columns:",  # we write the columns with our `csv` writer, above
        ]
    )


def to_json(results: list[Result], pretty: bool = True) -> str:
    """JSONify the given results."""
    if pretty:
        indent = 2
    else:
        indent = None
    return json.dumps(results, indent=indent)
