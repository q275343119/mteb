import requests


def get(url: str, params: str = None, verify: bool = False):
    return requests.get(url, params, verify=verify)


