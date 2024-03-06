from dataclasses import dataclass
from typing import Callable, TypeAlias

# An Extractor function takes a search key and a "local testing" flag and
# returns a list of Results.
SearchKey: TypeAlias = str
Result: TypeAlias = dict[str, str]
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
            # Probably need to revisit this once we deal in parallelism :') :') :')
            self.results += new_results
            self.results_success.add(key)
        else:
            self.results_not_found.add(key)
