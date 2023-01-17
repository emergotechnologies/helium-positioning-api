"""Models Module.

.. module:: Models

:synopsis: Classes and functions for the prediction of device positions

.. moduleauthor:: DSIA21

"""

import logging
from abc import abstractmethod
from typing import List

from helium_api_wrapper.DataObjects import IntegrationHotspot
from helium_api_wrapper.devices import get_last_integration

from helium_positioning_api.auxilary import midpoint
from helium_positioning_api.DataObjects import Prediction
from helium_positioning_api.distance_prediction import get_model
from helium_positioning_api.distance_prediction import predict_distance


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Model:
    """Base Model class."""

    @abstractmethod
    def predict(self, uuid: str, **kwargs) -> Prediction:
        """Return the position prediction of the model."""
        pass

    def get_hotspots(self, uuid: str) -> List[IntegrationHotspot]:
        """Load hotspots, which interacted with the given device from the last integration event."""
        integration = get_last_integration(uuid)
        if len(integration.hotspots) == 0:
            raise ValueError(f"No hotspots found for device {uuid}")
        return integration.hotspots


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
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)
        nearest_neighbor = sorted_hotspots[0]
        return Prediction(
            uuid=uuid,
            lat=nearest_neighbor.lat,
            lng=nearest_neighbor.lng,
            timestamp=nearest_neighbor.reported_at,
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
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)
        if len(sorted_hotspots) > 1:
            midpoint_lat, midpoint_long = midpoint(
                sorted_hotspots[0], sorted_hotspots[1]
            )
        else:
            logger.warning(
                "Not enough hotspots to perform Midpoint approximation."
                "Using nearest neighbor model instead."
            )
        return Prediction(uuid=uuid, lat=midpoint_lat, lng=midpoint_long)


class Trilateration(Model):
    """This model predicts the location of a given device using trilateration."""

    def predict(self, uuid: str, model: str) -> Prediction:
        """Create an object of Class Prediction.

        :param uuid: Device id
        :param model: Model to use for distance prediction

        :return: coordinates of predicted location
        """
        model = get_model(model)
        hotspots = self.get_hotspots(uuid)
        sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)

        if len(sorted_hotspots) < 3:
            logger.warning(
                "Not enough hotspots to perform trilateration. "
                "Using nearest neighbor model instead."
            )
            return NearestNeighborModel().predict(uuid)

        distance, longitude, latitude = [], [], []
        for hotspot in sorted_hotspots:
            dist = predict_distance(
                model,
                [
                    hotspot.lat,
                    hotspot.lng,
                    hotspot.rssi,
                    hotspot.snr,
                    hotspot.spreading,
                ],
            )
            longitude.append(hotspot.lng)
            latitude.append(hotspot.lat)
            distance.append(dist)

        hotspots = zip(latitude, longitude, distance, strict=False)

        # [[lat, long, dist], [lat, long, dist], [lat, long, dist]]

        # do trilateration

        # return Prediction(
        #     uuid=uuid,
        #     lat=nearest_neighbor.lat,
        #     lng=nearest_neighbor.long,
        #     timestamp=nearest_neighbor.reported_at,
        # )
