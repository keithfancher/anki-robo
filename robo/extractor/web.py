from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

DEFAULT_PARSER: str = "html.parser"


def get_page_data(
    key: str, url: str, local_testing: bool, local_path: str, encoding: str = "utf-8"
) -> BeautifulSoup:
    if local_testing:
        soup = get_local_page_data(key, local_path, encoding)
    else:
        soup = get_remote_page_data(url)
    return soup


def get_remote_page_data(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, DEFAULT_PARSER)
    return soup


# Get local HTML data instead of fetching from a URL. Look for a filename that
# matches the input "key" (with `.html` extension) in a directory that matches
# the extractor module path.
def get_local_page_data(key: str, path: str, enc: str) -> BeautifulSoup:
    # TODO: cleanup/normalize path concatenation
    newpath = "tests/testdata/" + path + f"/{key}.html"
    with open(newpath, encoding=enc) as fp:
        soup = BeautifulSoup(fp, DEFAULT_PARSER)
    return soup


def safe_string(tag: Optional[Tag]) -> str:
    """A wrapper for the BeautifulSoup Tag's `string` method, to make it less
    annoying to deal with the constant possibility of `None`. Consistently and
    safely returns a `str` value."""
    # Note that both `tag` AND `tag.string` can be `None` :')
    if tag and tag.string:
        return tag.string
    else:
        return ""


def safe_strings(tag: Optional[Tag]) -> list[str]:
    """A wrapper for the BeautifulSoup Tag's `strings` method, to make it less
    annoying to deal with the constant possibility of `None`. Consistently and
    safely returns a `list` of `str` values."""
    if tag and tag.strings:
        return list(tag.strings)
    else:
        return []
