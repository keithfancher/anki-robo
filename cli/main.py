import argparse

import robo


def from_text_file(filename: str, extractor_name: str, local_testing: bool) -> str:
    with open(filename, "r") as f:
        contents = f.read()
    results_summary = robo.from_plaintext(contents, extractor_name, local_testing)
    return robo.to_csv(results_summary.results)


def list_extractors_callback(args: argparse.Namespace) -> None:
    for extractor_name in robo.get_extractor_names():
        print(extractor_name)


def extract_callback(args: argparse.Namespace) -> None:
    local_testing = True  # TODO!
    try:
        r = from_text_file(args.infile, args.extractor, local_testing)
        print(r)
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
    parser_get.add_argument("extractor")
    parser_get.add_argument("infile")
    parser_get.set_defaults(func=extract_callback)

    args = parser.parse_args()
    args.func(args)
