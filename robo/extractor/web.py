import requests
from bs4 import BeautifulSoup


def get_page_data(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup