"""Nearest neighbor for the positioning API."""

import logging

from helium_positioning_api.auxilary import get_integration_hotspots
from helium_positioning_api.DataObjects import Prediction


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def nearest_neighbor(uuid: str) -> Prediction:
    """This model predicts the location of a given device.

    It takes the location of the nearest witness
    in terms of highest rssi recieved.

    :param uuid: Device id
    :return: coordinates of predicted location
    """
    hotspots = get_integration_hotspots(uuid)
    sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)
    neighbor = sorted_hotspots[0]
    return Prediction(
        uuid=uuid,
        lat=neighbor.lat,
        lng=neighbor.lng,
        # timestamp=neighbor.reported_at,
    )
