import logging
from datetime import timedelta
from time import sleep
from typing import Dict, Union

import requests
import requests_cache
from requests_cache.models.response import CachedResponse

from src import exceptions, setup

RequestParams = Dict[str, Union[str, int, float]]


def lastfm_get(params: RequestParams, cached: bool = False) -> requests.Response:
    """Base request"""
    logging.debug("Request with params:\n%s", params)

    # define headers and URL
    headers = {"user-agent": setup.LASTFM_API_USER}
    url = "http://ws.audioscrobbler.com/2.0/"

    # Add API key and format to the params
    params["api_key"] = setup.LASTFM_API_KEY
    params["format"] = "json"

    session = (
        requests.Session()
        if not cached
        else requests_cache.CachedSession(
            str(setup.PROJECT_ROOT / "cache" / "cache"),
            expire_after=timedelta(days=30),
            ignored_parameters=["api_key"],
        )
    )

    response = session.get(url, headers=headers, params=params, timeout=10)
    if not isinstance(response, CachedResponse):
        sleep(1)

    response.raise_for_status()

    if "error" in response.json():
        raise exceptions.LastfmError("Request error %s" % response.json())

    return response
