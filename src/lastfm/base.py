import logging
from typing import Dict, Union

import requests

from src import setup

RequestParams = Dict[str, Union[str, int, float]]


def lastfm_get(params: RequestParams) -> requests.Response:
    """Base request"""
    logging.debug("Request with params:\n%s", params)

    # define headers and URL
    headers = {"user-agent": setup.LASTFM_API_USER}
    url = "http://ws.audioscrobbler.com/2.0/"

    # Add API key and format to the params
    params["api_key"] = setup.LASTFM_API_KEY
    params["format"] = "json"

    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response
