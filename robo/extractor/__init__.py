from typing import Callable, TypeAlias

# Extract function takes a search key and returns a list of Results.
SearchKey: TypeAlias = str
Result: TypeAlias = dict[str, str]
Extractor: TypeAlias = Callable[[SearchKey], list[Result]]
