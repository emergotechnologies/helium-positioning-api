"""Midpoint prediction for the positioning API."""

import logging

from helium_positioning_api.auxilary import get_integration_hotspots
from helium_positioning_api.auxilary import get_midpoint
from helium_positioning_api.DataObjects import Prediction
from helium_positioning_api.nearest_neighbor import nearest_neighbor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def midpoint(uuid: str) -> Prediction:
    """This model predicts the location of a given device. \
    It approximates the midpoint of the two witnesses with the highest rssi.

    :param uuid: Device id

    :return: coordinates of predicted location
    """
    hotspots = get_integration_hotspots(uuid)
    sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)
    if len(sorted_hotspots) > 1:
        midpoint_lat, midpoint_long = get_midpoint(
            sorted_hotspots[0], sorted_hotspots[1]
        )
    else:
        logger.warning(
            "Not enough hotspots to perform Midpoint approximation."
            "Using nearest neighbor model instead."
        )
        return nearest_neighbor(uuid)
    return Prediction(uuid=uuid, lat=midpoint_lat, lng=midpoint_long)
