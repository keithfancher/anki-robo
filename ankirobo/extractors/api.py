import json
from pathlib import Path
from typing import Any

import requests


def api_post(
    key: str, url: str, data: dict, local_testing: bool, local_path: str
) -> Any:
    """Make the given POST request and return decoded JSON results. If
    `local_testing` is True, return static local data rather than hitting a
    remote endpoint."""
    if local_testing:
        json_resp = local_api_data(key, local_path)
    else:
        json_resp = post_remote_api_data(url, data)
    return json_resp


def post_remote_api_data(url: str, data: dict) -> Any:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise exception if status isn't 200/ok
    return response.json()


def local_api_data(key: str, path: str) -> Any:
    # TODO: factor out common testdata path logic
    newpath = Path("tests/testdata/" + path + f"/{key}.json")
    if newpath.exists():
        with newpath.open() as fp:
            json_resp = json.load(fp)
    else:
        json_resp = None
    return json_resp
