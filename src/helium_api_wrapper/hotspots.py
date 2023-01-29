"""Hotspot Module.

.. module:: helpers

:synopsis: Functions to load Hotspots from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import List

from helium_api_wrapper.DataObjects import Hotspot
from helium_api_wrapper.DataObjects import Role
from helium_api_wrapper.endpoint import request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_hotspot_by_address(address: str) -> List[Hotspot]:
    """Load a hotspot.

    :param address: Address of the hotspot
    :return: Hotspot
    """
    hotspot = request(url=f"hotspots/{address}", endpoint="api")
    return [Hotspot(**hotspot[0])]


def get_hotspots(pages: int = 1, filter_modes: str = "full") -> List[Hotspot]:
    """Load a list of hotspots.

    :param pages: Amount of pages to load
    :param filter_modes: Filter modes
    :return: List of hotspots
    """
    hotspots = request(
        url="hotspots/",
        endpoint="api",
        params={"filter_modes": filter_modes},
        pages=pages,
    )
    return [Hotspot(**i) for i in hotspots]


def load_roles(
    address: str, limit: int = 5, filter_types: str = "poc_receipts_v2"
) -> List[Role]:
    """Load roles for a hotspot.

    :param address: Address of the hotspot
    :param limit: Limit of roles to load
    :param filter_types: Filter types for roles
    :return: List of roles
    """
    roles = request(
        url=f"hotspots/{address}/roles",
        endpoint="api",
        params={"limit": limit, "filter_types": filter_types},
    )

    return [Role(**i) for i in roles]


def get_hotspots_box_search(
    swlat: str, swlon: str, nelat: str, nelon: str
) -> List[Hotspot]:
    """Get a list of hotspots by box search.

    :param swlat: The latitude of the southwest corner, defaults to None
    :type swlat: float

    :param swlon: The longitude of the southwest corner, defaults to None
    :type swlon: float

    :param nelat: The latitude of the northeast corner, defaults to None
    :type nelat: float

    :param nelon: The longitude of the northeast corner, defaults to None
    :type nelon: float

    :return: The hotspots.
    :rtype: list[Hotspot]
    """
    logger.info(f"Getting hotspots for box search {swlat}, {swlon}, {nelat}, {nelon}")
    hotspots = request(
        url="hotspots/location/box_search",
        endpoint="api",
        params={"swlat": swlat, "swlon": swlon, "nelat": nelat, "nelon": nelon},
    )
    return [Hotspot(**i) for i in hotspots]


def get_hotspots_by_position(lat: str, lon: str, distance: int) -> List[Hotspot]:
    """Get a list of hotspots by position.

    :param lat: The latitude of the position, defaults to None
    :type lat: float

    :param lon: The longitude of the position, defaults to None
    :type lon: float

    :param distance: The distance in meters, defaults to None
    :type distance: int

    :return: The hotspots.
    :rtype: list[Hotspot]
    """
    logger.info(f"Getting hotspots for position {lat}, {lon} within {distance} meters")
    hotspots = request(
        "hotspots/location/distance",
        params={"lat": lat, "lon": lon, "distance": distance},
    )
    return [Hotspot(**i) for i in hotspots]
