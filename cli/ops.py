from datetime import datetime

import ankirobo as robo


def extract(
    extractor_name: str, infile: str, opts: robo.RoboOpts, stdout: bool
) -> None:
    """The main `extract` operation. Ties the pieces together, extracts the
    data, and gives results back to the user."""
    print(
        f"Extracting data from source `{extractor_name}` using search keys from file: {infile}"
    )
    if opts.local_testing:
        print("\nWARNING: test flag is set to TRUE, using local test data only")
    print()

    try:
        r = from_text_file(infile, extractor_name, opts)
        show_results(r)
        write_output(r, extractor_name, stdout)
    except robo.InvalidExtractorName:
        print("Invalid extractor name: " + extractor_name)
    except FileNotFoundError:
        print("Input file not found: " + infile)


def extract_one(extractor_name: str, search_key: str, local_testing: bool) -> None:
    """Quick way to extract data for a single search key."""
    results = robo.extract_one(extractor_name, search_key, local_testing)
    print(robo.to_json(results))


def from_text_file(
    filename: str, extractor_name: str, opts: robo.RoboOpts
) -> robo.ResultSummary:
    """Extracts data for terms in given textfile."""
    with open(filename, "r") as f:
        contents = f.read()
    return robo.from_plaintext(contents, extractor_name, opts)


def show_results(results: robo.ResultSummary) -> None:
    """Summarize results for user."""
    success = results.results_success
    print(f"SUCCESS: {len(success)}")
    for s in success:
        print(f"\t{s}")

    not_found = results.results_not_found
    print(f"\nNOT FOUND: {len(not_found)}")
    for f in not_found:
        print(f"\t{f}")
    print()


def write_output(
    results: robo.ResultSummary, extractor_name: str, stdout: bool
) -> None:
    """Write output data to a file, or to stdout if that flag is specified."""
    csv_data = robo.to_csv(results.results, extractor_name)
    if stdout:
        print("CSV DATA:")
        print(csv_data, end="")
    else:
        ts = round(datetime.now().timestamp())
        filename = f"ankirobo-{extractor_name}-{ts}.csv"
        print(f"Writing CSV output to {filename}... ", end="")
        with open(filename, "w") as f:
            f.write(csv_data)
        print("Complete!")
