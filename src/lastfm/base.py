import logging
from time import sleep
from typing import Dict, Union

import requests
from joblib import Memory

from src import exceptions, setup

RequestParams = Dict[str, Union[str, int, float]]

memory = Memory("./cache", verbose=0)


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
    sleep(1)
    response.raise_for_status()

    if "error" in response.json():
        raise exceptions.LastfmError("Request error %s" % response.json())

    return response


@memory.cache
def lastfm_get_w_caching(*args, **kwargs):
    res = lastfm_get(*args, **kwargs)
    return res
