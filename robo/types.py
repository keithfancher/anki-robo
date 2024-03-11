from dataclasses import dataclass
from typing import Callable, TypeAlias

# A search key is just a string. (This alias is just for explicitness in type
# signatures. You don't have to use it.)
SearchKey: TypeAlias = str

# A `Result` is just a map from string -> string, corresponding to "Anki card
# field name" -> "Anki card field value". As you might guess, one `Result`
# corresponds to one Anki card.
Result: TypeAlias = dict[str, str]

# An `Extractor` is just a function! At its heart, it's a function that takes a
# single search key and returns a list of results. However, there's also a
# "local testing" flag which the function can use to change its behavior, if
# need be.
#
# If you're not used to the `Callable` syntax, it's analogous to a function
# that looks like this:
#
#     def extract(key: str, local_testing: bool) -> list[Result]:
Extractor: TypeAlias = Callable[[SearchKey, bool], list[Result]]


class InvalidExtractorName(Exception):
    pass


@dataclass
class ResultSummary:
    """A wrapper for results data and success/failure info."""

    # The actual results data.
    results: list[Result]
    # Set of keys for which data was found by the extractor.
    results_success: set[str]  # TODO: Just a dict, maybe? Depends how I use it...
    # Set of keys for which data was NOT found by the extractor.
    results_not_found: set[str]

    def append(self, key: str, new_results: list[Result]) -> None:
        """Append a new set of results to the summary. Keep track of empty
        results and successes."""
        if new_results:
            # I guess mutable state is the way in Python? :')
            self.results += new_results
            self.results_success.add(key)
        else:
            self.results_not_found.add(key)
