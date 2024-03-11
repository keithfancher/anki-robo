import argparse
from datetime import datetime

import robo


def from_text_file(
    filename: str, extractor_name: str, opts: robo.RoboOpts
) -> robo.ResultSummary:
    with open(filename, "r") as f:
        contents = f.read()
    return robo.from_plaintext(contents, extractor_name, opts)


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


def make_opts(args: argparse.Namespace) -> robo.RoboOpts:
    if args.parallel < 0:
        raise ValueError("`parallel` value must be >= 0")
    elif args.parallel == 0:
        # 0 on the CLI is equivalent to `None`, aka "let Python decide the limit"
        args.parallel = None
    return robo.RoboOpts(
        local_testing=args.test, max_parallel=args.parallel, limit=None
    )


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
        r = from_text_file(args.infile, args.extractor, make_opts(args))
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
    parser_list.set_defaults(callback=list_extractors_callback)

    # `get` subcommand: get Anki data with a given extractor
    parser_get = subparsers.add_parser(
        "get", aliases=["g"], help="Get Anki card data with the given extractor"
    )
    parser_get.add_argument(
        "extractor",
        metavar="EXTRACTOR_NAME",
        help="The extractor to use. See all extractors with the `list` command.",
    )
    parser_get.add_argument(
        "infile",
        metavar="INPUT_FILE",
        help="Name of a file with newline-delimited input search keys.",
    )
    parser_get.add_argument(
        "-s",
        "--stdout",
        help="write output CSV to standard out instead of a file",
        action="store_true",
    )
    parser_get.add_argument(
        "-t",
        "--test",
        help="test using static local data rather than making remote calls",
        action="store_true",
    )
    parser_get.add_argument(
        "-p",
        "--parallel",
        type=int,
        metavar="NUM_WORKERS",
        default=robo.DEFAULT_MAX_WORKERS,
        help=f"maximum number of workers running in parallel (default is {robo.DEFAULT_MAX_WORKERS}; use 0 for Python's default limit, which depends on your CPU)",
    )
    parser_get.set_defaults(callback=extract_callback)

    # If the user passes *no* commands, e.g. just calls `./ankirobo`, it somehow
    # is treated as a valid case, but the `callback` property doesn't exist, so
    # this throws. That seems broken to me? This workaround is fine for now.
    args = parser.parse_args()
    if hasattr(args, "callback"):
        args.callback(args)
    else:
        print("Please provide a command! Try -h for usage information :D")
