import logging

import requests

from src import setup


def lastfm_get(payload):
    """Base request"""
    logging.debug(f"Request with params:\n{payload}")

    # define headers and URL
    headers = {"user-agent": setup.LASTFM_API_USER}
    url = "http://ws.audioscrobbler.com/2.0/"

    # Add API key and format to the payload
    payload["api_key"] = setup.LASTFM_API_KEY
    payload["format"] = "json"

    response = requests.get(url, headers=headers, params=payload)
    return response
