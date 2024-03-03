import requests
from bs4 import BeautifulSoup


def get_page_data(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


# Get local HTML data instead of fetching from a URL. Look for a filename that
# matches the input "key" (with `.html` extension) in a directory that matches
# the extractor module path.
def get_local_page_data(key: str, path: str, enc: str) -> BeautifulSoup:
    newpath = "tests/testdata/" + path + f"/{key}.html"
    with open(newpath, encoding=enc) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup
