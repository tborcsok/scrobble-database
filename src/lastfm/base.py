import logging
from datetime import timedelta
from time import sleep
from typing import Dict, Union

import requests
import requests_cache
from requests_cache.models.response import CachedResponse
from tenacity import retry, retry_if_exception_message, stop_after_attempt, wait_fixed

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

    response = make_request(url=url, headers=headers, params=params, session=session)

    # some requests are successful, but contain error info in the JSON
    if "error" in response.json():
        raise exceptions.LastfmError("Request error %s" % response.json())

    return response


@retry(retry=retry_if_exception_message(match="500"), wait=wait_fixed(5), stop=stop_after_attempt(3))
def make_request(
    url: str, headers: dict[str, str], params: dict[str, str], session: requests.Session | requests_cache.CachedSession
) -> requests.Response | CachedResponse:
    """Request function with retry logic for HTTP error 500 Internal Server Error"""

    response = session.get(url, headers=headers, params=params, timeout=10)

    if not isinstance(response, CachedResponse):
        sleep(1)

    response.raise_for_status()

    return response
