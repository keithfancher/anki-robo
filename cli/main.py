import argparse
from datetime import datetime

import robo


def from_text_file(
    filename: str, extractor_name: str, local_testing: bool
) -> robo.ResultSummary:
    with open(filename, "r") as f:
        contents = f.read()
    return robo.from_plaintext(contents, extractor_name, local_testing)


def show_results(results: robo.ResultSummary) -> None:
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
    csv_data = robo.to_csv(results.results)
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


def list_extractors_callback(args: argparse.Namespace) -> None:
    for extractor_name in robo.get_extractor_names():
        print(extractor_name)


def extract_callback(args: argparse.Namespace) -> None:
    print(
        f"Extracting data from source `{args.extractor}` using search keys from file: {args.infile}"
    )
    if args.test:
        print("\nWARNING: test flag is set to TRUE, using local test data only")
    print()

    try:
        r = from_text_file(args.infile, args.extractor, args.test)
        show_results(r)
        write_output(r, args.extractor, args.stdout)
    except robo.InvalidExtractorName:
        print("Invalid extractor name: " + args.extractor)
    except FileNotFoundError:
        print("Input file not found: " + args.infile)


def main() -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="Available anki-robo commands")

    # `list` subcommand: show all available extractors
    parser_list = subparsers.add_parser(
        "list", aliases=["l"], help="List all available data extractors"
    )
    parser_list.set_defaults(func=list_extractors_callback)

    # `get` subcommand: get Anki data with a given extractor
    parser_get = subparsers.add_parser(
        "get", aliases=["g"], help="Get Anki card data with the given extractor"
    )
    parser_get.add_argument(
        "extractor",
        help="The extractor to use. See all extractors with the `list` command.",
    )
    parser_get.add_argument(
        "infile", help="Name of a file with newline-delimited input search keys."
    )
    parser_get.add_argument(
        "-s",
        "--stdout",
        help="Write output CSV to standard out instead of a file",
        action="store_true",
    )
    parser_get.add_argument(
        "-t",
        "--test",
        help="Test using static local data rather than making remote calls",
        action="store_true",
    )
    parser_get.set_defaults(func=extract_callback)

    # If the user passes *no* commands, e.g. just calls `./ankirobo`, it
    # somehow is treated as a valid case, but the `func` callback doesn't exist
    # so this throws. That seems broken to me? This workaround is fine for now.
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Please provide a command! Try -h for usage information :D")
