"""Models Module.

.. module:: Models

:synopsis: Classes and functions for the prediction of device positions

.. moduleauthor:: DSIA21

"""

import logging
from abc import abstractmethod
from typing import List

from haversine import haversine
from haversine import Unit

from helium_api_wrapper.DataObjects import IntegrationHotspot
from helium_api_wrapper.devices import get_last_integration

from helium_positioning_api.auxilary import circle_intersect
from helium_positioning_api.auxilary import flatten_intersect_lists
from helium_positioning_api.auxilary import get_centres
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
    """Predicts the location of a given device using trilateration."""

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
        m = Unit.METERS
        # [[lat, long, dist], [lat, long, dist], [lat, long, dist]]

        # do trilateration
        c_0, c_1, c_2, ind = get_centres(latitude, longitude)
        # generating intersects and checking for their existence
        tol = 25  # tol in meters
        if len(circle_intersect(c_0, distance[ind[0]], c_1, distance[ind[1]])) > 0:
            intersects_0_1 = []
            intersect_0_1_a, intersect_0_1_b = circle_intersect(
                c_0, distance[ind[0]], c_1, distance[ind[1]]
                )
            if haversine(intersect_0_1_a, intersect_0_1_b, m) < 10:
                intersects_0_1.append(midpoint(
                    intersect_0_1_a, intersect_0_1_b)
                    )
            else:
                intersects_0_1 += [intersect_0_1_a, intersect_0_1_b]
        if len(circle_intersect(c_0, distance[ind[0]], c_2, distance[ind[2]])) > 0:
            intersects_0_2 = []
            intersect_0_2_a, intersect_0_2_b = circle_intersect(c_0, distance[ind[0]], c_2, distance[ind[2]])
            if haversine(intersect_0_2_a, intersect_0_2_b, m) < 10:
                intersects_0_2.append(midpoint(intersect_0_2_a, intersect_0_2_b))
            else:
                intersects_0_2 += [intersect_0_2_a, intersect_0_2_b]
        if len(circle_intersect(c_1, distance[ind[1]], c_2, distance[ind[2]])) > 0:
            intersects_1_2 = []
            intersect_1_2_a, intersect_1_2_b = circle_intersect(c_1, distance[ind[1]], c_2, distance[ind[2]])
            if haversine(intersect_1_2_a, intersect_1_2_b, m) < 10:
                intersects_1_2.append(midpoint(intersect_1_2_a, intersect_1_2_b))
            else:
                intersects_1_2 += [intersect_1_2_a, intersect_1_2_b]
        # removing none - intersects
        intersects = [intersects_0_1, intersects_0_2, intersects_1_2]
        for i in range(len(intersects)):
            intersects[i] = [p for p in intersects[i] if p is not None]

        # classifying intersects
        empty_intersects = []
        two_intersection_points = []
        singular_points = []
        for i in range(3):
            if len(intersects[i]) == 1:
                singular_points.append(intersects[i])
            elif len(intersects[i]) == 0:
                empty_intersects.append(intersects[i])
            elif len(intersects[i]) == 2:
                two_intersection_points.append(intersects[i])

        if empty_intersects is not None:
            empty_intersects = flatten_intersect_lists(empty_intersects)
        else:
            empty_intersects = []

        if singular_points is not None:
            singular_points = flatten_intersect_lists(singular_points)
        else:
            singular_points = []

        if two_intersection_points is None:
            two_intersection_points = []

        # estimation proper
        if len(singular_points) == 1 & len(two_intersection_points) == 0:
            estimated_position = singular_points[0]

        elif len(singular_points) == 2:

            if haversine(singular_points[0], singular_points[1], unit=m) < tol:
                estimated_position = midpoint(singular_points[0], singular_points[1])
            else:
                for singular in singular_points:
                    for two_int in two_intersection_points:
                        for i in range(2):
                            if haversine(singular, two_int[i], unit=m):
                                estimated_position = midpoint(singular, two_int[i])

        elif len(singular_points) == 3:
            if haversine(singular_points[0], singular_points[1], unit=m) < tol:
                first_mid = midpoint(singular_points[0], singular_points[1])
                if haversine(first_mid, singular_points[2], unit=m) < tol:
                    second_mid = midpoint(first_mid, singular_points[2])
                    estimated_position = second_mid
                else:
                    estimated_position = first_mid
            elif haversine(singular_points[0], singular_points[2], unit=m) < tol:
                first_mid = midpoint(singular_points[0], singular_points[2])
                if haversine(first_mid, singular_points[1], unit=m) < tol:
                    second_mid = midpoint(first_mid, singular_points[1])
                    estimated_position = second_mid
                else:
                    estimated_position = first_mid
            elif haversine(singular_points[1], singular_points[2], unit=m) < tol:
                first_mid = midpoint(singular_points[1], singular_points[2])
                if haversine(first_mid, singular_points[0], unit=m) < tol:
                    second_mid = midpoint(first_mid, singular_points[0])
                    estimated_position = second_mid
                else:
                    estimated_position = first_mid

        elif len(two_intersection_points) > 1:
            candidates = []  # list of points that are close enough to the others
            for h in range(2):
                candidate_1 = two_intersection_points[0][h]
                for i in range(len(two_intersection_points) - 1):
                    for j in range(2):
                        candidate_2 = two_intersection_points[i + 1][j]
                        if haversine(candidate_1, candidate_2, unit=m) < tol:
                            candidates.append(midpoint(candidate_1, candidate_2))
            if len(candidates) == 2:
                estimated_position = midpoint(candidates[0], candidates[1])
            elif len(candidates) == 1:
                estimated_position = candidates[0]
            elif len(candidates) == 0:
                all_intersects = sum(two_intersection_points, [])
                if len(all_intersects) > 1:
                    # Looking for the two intersections with the min distance
                    distance = haversine(all_intersects[0], all_intersects[1], m)
                    first_point = all_intersects[0]
                    second_point = all_intersects[1]
                    for i in range(len(all_intersects)):
                        for j in range(i + 1, len(all_intersects)):
                            if haversine(all_intersects[i], all_intersects[j], m) < distance:
                                first_point = all_intersects[i]
                                second_point = all_intersects[j]
                                distance = haversine(first_point, second_point, m)
                estimated_position = midpoint(first_point, second_point)

        elif len(two_intersection_points) == 1:
            # choose ISP with the shortest distnance to its furthest hotspot
            centres = [c_0, c_1, c_2]
            candidate_1 = two_intersection_points[0][0]
            candidate_2 = two_intersection_points[0][1]

            distances_1, distances_2 = [], []
            for centre in centres:
                distances_1.append(haversine(candidate_1, centre, unit=m))
                distances_2.append(haversine(candidate_2, centre, unit=m))
            max_1 = max(distances_1)
            max_2 = max(distances_2)

            if max_1 < max_2:
                estimated_position = candidate_1
            else:
                estimated_position = candidate_2

        # TODO en(empty_intersects) == 3 INTERSECTIONS over other indices

        return Prediction(
            uuid=uuid,
            lat=estimated_position[0],
            lng=estimated_position[1],
            timestamp=Trilateration.reported_at,
         )
