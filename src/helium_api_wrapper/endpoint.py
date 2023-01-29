"""Endpoint Module.

.. module:: Endpoint

:synopsis: Classes and functions for Helium API Endpoint

.. moduleauthor:: DSIA21

"""

import logging
import os
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import requests
from dotenv import find_dotenv
from dotenv import load_dotenv
from requests import Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def request(
    url: str,
    endpoint: str = "api",
    params: Optional[Dict[str, Any]] = None,
    pages: int = 1,
) -> List[Dict[str, Any]]:
    """Handle request to Helium API.

    :param url: The url to request
    :param endpoint: The endpoint to request. Either "api" or "console".
    :param params: The parameters to send with the request
    :param pages: The number of pages to request
    :return: The response from the API
    """
    # assert endpoint in ["api", "console"], "Endpoint should be either api or console."
    url = __get_url(url=url, endpoint=endpoint)
    headers = __get_headers(endpoint=endpoint)
    params = params or {}

    data = []

    for page in range(pages):
        res = __request_with_exponential_backoff(
            url=url, headers=headers, params=params
        )
        if res["cursor"] == "":
            logger.debug(f"Finished crawling data at page {page + 1} of {pages}.")
            break

        if isinstance(res["data"], list):
            data.extend(res["data"])
        else:
            data.append(res["data"])

    return data


def __get_headers(endpoint: str) -> Dict[str, str]:
    headers = {"User-Agent": "HeliumPythonWrapper/0.3.1"}
    if endpoint == "console":
        # if package is installed globally look for .env in cwd
        if not (dotenv_path := find_dotenv()):
            dotenv_path = find_dotenv(usecwd=True)

        load_dotenv(dotenv_path)
        api_key = os.getenv("API_KEY")

        if api_key is None or api_key == "":
            raise Exception("No api key found in .env")
        headers["key"] = os.getenv("API_KEY")
    return headers


def __request_with_exponential_backoff(
    url: str, headers: Dict[str, str], params: Dict[str, Any], max_retries: int = -1
) -> Dict[str, Any]:
    """Send a request and retry with exponential backoff.

    if the response code is in the error_codes list.

    :param url: The url to request
    :param headers: The headers to send with the request
    :param params: The parameters to send with the request
    :param max_retries: The maximum number of retries. -1 means infinite retries.

    :return: The response from the API
    :return: None
    """
    response = __request(url=url, headers=headers, params=params)
    error_codes = [429, 500, 502, 503]
    exponential_sleep_time = 1
    num_of_retries = 0
    is_error = response.status_code in error_codes
    while (is_error and max_retries == -1) or (
        is_error and num_of_retries < max_retries
    ):
        num_of_retries += 1
        logger.info(
            f"Got status code {response.status_code}"
            f"Sleeping for {exponential_sleep_time} seconds"
        )
        exponential_sleep_time = min(600, exponential_sleep_time * 2)
        time.sleep(exponential_sleep_time)
        response = __request(url=url, headers=headers, params=params)
        is_error = response.status_code in error_codes

    if response.status_code in error_codes:
        raise Exception(f"Request failed with status code {response.status_code}")
    else:
        return __handle_response(response)


def __handle_response(response: requests.Response) -> Dict[str, Any]:
    """Handle the response from the Helium API."""
    data = {"data": None, "cursor": None}
    if response.status_code == 404:
        logger.warning("Resource not found")
        return data

    if response.status_code == 204:
        logger.warning("No content")
        return data
    else:
        r = response.json()

    if response.status_code == 200:
        if "cursor" in r:
            data["cursor"] = r["cursor"]

        if "data" not in r:
            data["data"] = r
        else:
            data["data"] = r["data"]

        return data

    else:
        raise Exception(f"Request failed with status code {response.status_code}")


def __request(url: str, params: Dict[str, str], headers: Dict[str, str]) -> Response:
    """Send a simple request to the Helium API and return the response."""
    logger.debug(f"Requesting {url}...")
    response = requests.request(
        "GET",
        url=url,
        params=params,
        headers=headers,
    )
    return response


def __get_url(url: str, endpoint: str) -> str:
    """Get the URL for the endpoint.

    :return: The URL for the endpoint.
    """
    if endpoint == "console":
        # TODO: load from .env
        return f"https://{endpoint}.helium.com/api/v1/{url}"
    else:
        return f"https://{endpoint}.helium.io/v1/{url}"
