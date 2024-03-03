from typing import Callable, TypeAlias

# An Extractor function takes a search key and a "local testing" flag and
# returns a list of Results.
SearchKey: TypeAlias = str
Result: TypeAlias = dict[str, str]
Extractor: TypeAlias = Callable[[SearchKey, bool], list[Result]]
