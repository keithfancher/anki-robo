import argparse
from typing import Optional

import ankirobo as robo
import cli.ops as ops


def parse(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse the given CLI args. If `None`, defaults to `sys.argv`."""
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="Available anki-robo commands")
    add_list_command_parser(subparsers)
    add_get_command_parser(subparsers)
    add_one_command_parser(subparsers)

    return parser.parse_args(args)


def add_get_command_parser(subparsers) -> None:
    """Note: changes `subparsers` parameter in-place :')"""
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


def add_one_command_parser(subparsers) -> None:
    """Note: changes `subparsers` parameter in-place :')"""
    # `one` subcommand: extract data for a single search key
    parser_one = subparsers.add_parser(
        "one", aliases=["o"], help="Get data for a single search key"
    )
    # TODO: factor out the shared arguments?
    parser_one.add_argument(
        "extractor",
        metavar="EXTRACTOR_NAME",
        help="The extractor to use. See all extractors with the `list` command.",
    )
    parser_one.add_argument(
        "search_key",
        metavar="SEARCH_KEY",
        help="The search key to fetch data for.",
    )
    parser_one.add_argument(
        "-t",
        "--test",
        help="test using static local data rather than making remote calls",
        action="store_true",
    )
    parser_one.set_defaults(callback=extract_single_callback)


def add_list_command_parser(subparsers) -> None:
    """Note: changes `subparsers` parameter in-place :')"""
    # `list` subcommand: show all available extractors
    parser_list = subparsers.add_parser(
        "list", aliases=["l"], help="List all available data extractors"
    )
    parser_list.set_defaults(callback=list_extractors_callback)


def make_opts(parsed_args: argparse.Namespace) -> robo.RoboOpts:
    """Map from parsed CLI args to `RoboOpts` type."""
    if parsed_args.parallel < 0:
        raise ValueError("`parallel` value must be >= 0")
    elif parsed_args.parallel == 0:
        # 0 on the CLI is equivalent to `None`, aka "let Python decide the limit"
        parsed_args.parallel = None
    return robo.RoboOpts(
        local_testing=parsed_args.test, max_parallel=parsed_args.parallel, limit=None
    )


def list_extractors_callback(args: argparse.Namespace) -> None:
    for extractor_name in robo.get_extractor_names():
        print(extractor_name)


def extract_callback(args: argparse.Namespace) -> None:
    ops.extract(args.extractor, args.infile, make_opts(args), args.stdout)


def extract_single_callback(args: argparse.Namespace) -> None:
    ops.extract_one(args.extractor, args.search_key, args.test)
