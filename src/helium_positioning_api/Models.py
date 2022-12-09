"""Positioning Models module"""
from abc import abstractmethod
from typing import List
from helium_api_wrapper.devices import get_last_integration
from helium_positioning_api.auxilary import midpoint
from helium_positioning_api.DataObjects import Hotspot
from helium_positioning_api.DataObjects import Prediction


class Model:
    """Base Model class."""

    @abstractmethod
    def predict(self, uuid: str) -> Prediction:
        """Return the position prediction of the model."""
        pass

    def get_hotspots(self, uuid: str) -> List[Hotspot]:
        """Load interacting hotspots from last integration event."""
        integration = get_last_integration(uuid)
        return [Hotspot(**h) for h in integration.data["req"]["body"]["hotspots"]]


class NearestNeighborModel(Model):
    """This model predicts the location of a given device.

    It takes the location of the nearest witness
    in terms of highest rssi recieved.
    """

    def __init__(self) -> None:
        """Initialize an object of Class NearestNeighborModel."""
        pass

    def predict(self, uuid: str) -> Prediction:
        """Create Prediction using features of Hotspot with specified uuid.

        :param uuid: Device id

        :return: coordinates of predicted location
        """
        hotspots = self.get_hotspots(uuid)
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)  # type: ignore
        nearest_neighbor = sorted_hotspots[0]
        nearest_neighbor.load_location()
        return Prediction(
            uuid=uuid, lat=nearest_neighbor.lat, lng=nearest_neighbor.long
        )


class Midpoint(Model):
    """This model predicts the location of a given device. \
    It approximates the midpoint of the two witnesses with the highest rssi."""

    def __init__(self) -> None:
        """Initialize an object of class Midpoint."""
        pass

    def predict(self, uuid: str) -> Prediction:
        """Create an object of Class Prediction.

        :param uuid: Device id

        :return: coordinates of predicted location
        """
        hotspots = self.get_hotspots(uuid)
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)  # type: ignore
        assert len(sorted_hotspots) > 1, "Not enough witnesses"
        midpoint_lat, midpoint_long = midpoint(sorted_hotspots[0], sorted_hotspots[1])
        return Prediction(uuid=uuid, lat=midpoint_lat, lng=midpoint_long)
