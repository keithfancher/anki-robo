from typing import Optional

import ankirobo.cli.args as args


def main(cli_args: Optional[list[str]] = None) -> None:
    parsed_args = args.parse(cli_args)

    # If the user passes *no* commands, e.g. just calls `./anki-robo`, it somehow
    # is treated as a valid case, but the `callback` property doesn't exist, so
    # this throws. That seems broken to me? This workaround is fine for now.
    if hasattr(parsed_args, "callback"):
        parsed_args.callback(parsed_args)
    else:
        print("Please provide a command! Try -h for usage information :D")
