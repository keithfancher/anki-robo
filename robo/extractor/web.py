import requests
from bs4 import BeautifulSoup

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
