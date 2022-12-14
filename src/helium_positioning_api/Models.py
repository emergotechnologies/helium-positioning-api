"""Models Module.

.. module:: Models

:synopsis: Classes and functions for the prediction of device positions

.. moduleauthor:: DSIA21

"""

from abc import ABCMeta
from abc import abstractmethod
from typing import List

from helium_api_wrapper.helpers import load_last_integration

from helium_positioning_api.DataObjects import Hotspot
from helium_positioning_api.DataObjects import Prediction


class Model:
    """Base Model class."""

    @abstractmethod
    def predict(self, uuid: str) -> Prediction:
        """Return the position prediction of the model."""
        pass

    def get_hotspots(self, uuid: str) -> List[Hotspot]:
        """Load hotspots, which interacted with the given device from the last integration event."""
        integration = load_last_integration(uuid)
        print(integration)
        return [Hotspot(**h) for h in integration["data"]["req"]["body"]["hotspots"]]


class NearestNeighborModel(Model):
    """This model predicts the location of a given device, by taking the location of the nearest witness in terms of highest rssi recieved."""

    def __init__(self) -> None:
        pass

    def predict(self, uuid: str) -> Prediction:
        hotspots = self.get_hotspots(uuid)
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)
        nearest_neighbor = sorted_hotspots[0]
        nearest_neighbor.load_location()
        return Prediction(
            uuid=uuid,
            lat=nearest_neighbor.lat,
            lng=nearest_neighbor.long,
            timestamp=nearest_neighbor.reported_at,
        )
