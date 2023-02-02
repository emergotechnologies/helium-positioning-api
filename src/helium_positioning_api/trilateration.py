"""Trilateration for the positioning API."""

import logging
from typing import Any
from typing import List
from typing import Tuple

from haversine import Unit
from haversine import haversine
from helium_api_wrapper.DataObjects import IntegrationHotspot

from helium_positioning_api.auxilary import circle_intersect
from helium_positioning_api.auxilary import flatten_intersect_lists
from helium_positioning_api.auxilary import get_centres
from helium_positioning_api.auxilary import get_integration_hotspots
from helium_positioning_api.auxilary import mid
from helium_positioning_api.DataObjects import Prediction
from helium_positioning_api.distance_prediction import predict_distance
from helium_positioning_api.nearest_neighbor import nearest_neighbor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tol = 25  # tol in meters
m = Unit.METERS


def trilateration(uuid: str, model: str) -> Prediction:
    """Predicts the location of a given device using trilateration.

    :param uuid: Device id
    :param model: Model to use for distance prediction

    :return: coordinates of predicted location
    """
    hotspots = get_integration_hotspots(uuid)
    sorted_hotspots = sorted(hotspots, key=lambda h: h.rssi)

    if len(sorted_hotspots) < 3:
        logger.warning(
            "Not enough hotspots to perform trilateration. "
            "Using nearest neighbor model instead."
        )
        return nearest_neighbor(uuid)

    longitudes, latitudes, distances = compile_hotspot_info(sorted_hotspots, model)
    # calculating intersects
    centres, intersects = do_intersrect(latitudes, longitudes, distances)
    # classifying intersects
    empty_intersects, two_intersection_points, singular_points = classify_intersects(
        intersects
    )
    # estimation proper
    estimated_position = estimate_trilateration(
        empty_intersects, two_intersection_points, singular_points, centres, uuid
    )

    return Prediction(uuid=uuid, lat=estimated_position[0], lng=estimated_position[1])


def compile_hotspot_info(
    sorted_hotspots: List[IntegrationHotspot], model: str
) -> Tuple[List[float], List[float], List[float]]:
    """Return estimated distance and locations of hotspots.

    :param sorted_hotspots: List of hotspots sorted by signal quality
    :param model: Model to use for distance prediction

    :return: longitudes, latitudes, distances of said hotspots as list
    """
    distances, longitudes, latitudes = [], [], []
    for hotspot in sorted_hotspots:
        dist = predict_distance(
            model,
            {
                "snr": [hotspot.snr],
                "rssi": [hotspot.rssi],
                "datarate": [hotspot.datarate],
                "frequency": [hotspot.frequency],
            },
        )
        longitudes.append(hotspot.lng)
        latitudes.append(hotspot.lat)
        distances.append(dist)

    # hotspots = zip(latitudes, longitudes, distances, strict=False)
    return longitudes, latitudes, distances


def do_intersrect(
    latitude: List[float],
    longitude: List[float],
    distance: List[float],
    indices: Tuple[int, int, int] = (0, 1, 2),
) -> Tuple[List[Any], List[List[Any]]]:
    """Generates intersections of every circle.

    :param latitude: List of latitudes
    :param longitude: List of longitudes
    :param distance: List of distances
    :param indices: indices of circles to be intersected

    :return: list of centres and intersections
    """
    c_0, c_1, c_2, ind = get_centres(latitude, longitude, indices)
    centres = [c_0, c_1, c_2]
    # generating intersects and checking for their existence

    if len(circle_intersect(c_0, distance[ind[0]], c_1, distance[ind[1]])) > 0:
        intersects_0_1 = []
        intersect_0_1_a, intersect_0_1_b = circle_intersect(
            c_0, distance[ind[0]], c_1, distance[ind[1]]
        )
        if haversine(intersect_0_1_a, intersect_0_1_b, m) < 10:
            intersects_0_1.append(mid(intersect_0_1_a, intersect_0_1_b))
        else:
            intersects_0_1 += [intersect_0_1_a, intersect_0_1_b]
    if len(circle_intersect(c_0, distance[ind[0]], c_2, distance[ind[2]])) > 0:
        intersects_0_2 = []
        intersect_0_2_a, intersect_0_2_b = circle_intersect(
            c_0, distance[ind[0]], c_2, distance[ind[2]]
        )
        if haversine(intersect_0_2_a, intersect_0_2_b, m) < 10:
            intersects_0_2.append(mid(intersect_0_2_a, intersect_0_2_b))
        else:
            intersects_0_2 += [intersect_0_2_a, intersect_0_2_b]
    if len(circle_intersect(c_1, distance[ind[1]], c_2, distance[ind[2]])) > 0:
        intersects_1_2 = []
        intersect_1_2_a, intersect_1_2_b = circle_intersect(
            c_1, distance[ind[1]], c_2, distance[ind[2]]
        )
        if haversine(intersect_1_2_a, intersect_1_2_b, m) < 10:
            intersects_1_2.append(mid(intersect_1_2_a, intersect_1_2_b))
        else:
            intersects_1_2 += [intersect_1_2_a, intersect_1_2_b]
    # removing none - intersects
    intersects = [intersects_0_1, intersects_0_2, intersects_1_2]
    for i in range(len(intersects)):
        intersects[i] = [p for p in intersects[i] if p is not None]
    return centres, intersects


def classify_intersects(
    intersects: List[List[Any]],
) -> Tuple[List[List[Any]], List[List[Any]], List[List[Any]]]:
    """Classifies intersections of circles.

    :param intersects: list of intersection points

    :return: Lists of classified intersections
    """
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

    if len(empty_intersects) != 0:
        empty_intersects = flatten_intersect_lists(empty_intersects)

    if len(singular_points) != 0:
        singular_points = flatten_intersect_lists(singular_points)

    return empty_intersects, two_intersection_points, singular_points


def estimate_trilateration(
    empty_intersects: List[List[Any]],
    two_intersection_points: List[List[float]],
    singular_points: List[List[Any]],
    centres: List[float],
    uuid: str,
) -> Tuple[float, float]:
    """Provides position estimate.

    :param empty_intersects: list of empty intersects
    :param two_intersection_points: list of two intersections between two circles
    :param singular_points: list of singular intersections between two circles
    :param centres: hotspot locations (centres of circles)

    :return: Prediction
    """
    if len(singular_points) == 1 & len(two_intersection_points) == 0:
        estimated_position = singular_points[0]

    elif len(singular_points) == 2:
        estimated_position = two_singular_handler(
            singular_points, two_intersection_points
        )

    elif len(singular_points) == 3:
        estimated_position = three_singular_handler(singular_points)

    elif len(two_intersection_points) > 1:
        estimated_position = multiple_two_int_handler(two_intersection_points)

    elif len(two_intersection_points) == 1:
        estimated_position = singular_two_int_handler(two_intersection_points, centres)

    # TODO en(empty_intersects) == 3 INTERSECTIONS over other indices
    return estimated_position


def two_singular_handler(
    singular_points: List[List[float]], two_intersection_points: List[List[float]]
) -> List[Any]:
    """Calculate estimation when two out of three circles intersect in singular point.

    :param singular_points: points of singular intersection
    :param two_intersection_points: intersection points of circles intersecting in two places

    :return: position estimation
    """
    if haversine(singular_points[0], singular_points[1], unit=m) < tol:
        estimated_position = mid(singular_points[0], singular_points[1])
    else:
        for singular in singular_points:
            for two_int in two_intersection_points:
                for i in range(2):
                    if haversine(singular, two_int[i], unit=m):
                        estimated_position = mid(singular, two_int[i])
    return estimated_position


def three_singular_handler(singular_points: List[List[Any]]) -> List[Any]:
    """Calculate estimation when all intersects result in singular point.

    :param singular_points: points of singular intersection

    :return: position estimation
    """
    if haversine(singular_points[0], singular_points[1], unit=m) < tol:
        first_mid = mid(singular_points[0], singular_points[1])
        if haversine(first_mid, singular_points[2], unit=m) < tol:
            second_mid = mid(first_mid, singular_points[2])
            estimated_position = second_mid
        else:
            estimated_position = first_mid
    elif haversine(singular_points[0], singular_points[2], unit=m) < tol:
        first_mid = mid(singular_points[0], singular_points[2])
        if haversine(first_mid, singular_points[1], unit=m) < tol:
            second_mid = mid(first_mid, singular_points[1])
            estimated_position = second_mid
        else:
            estimated_position = first_mid
    elif haversine(singular_points[1], singular_points[2], unit=m) < tol:
        first_mid = mid(singular_points[1], singular_points[2])
        if haversine(first_mid, singular_points[0], unit=m) < tol:
            second_mid = mid(first_mid, singular_points[0])
            estimated_position = second_mid
        else:
            estimated_position = first_mid
    else:
        estimated_position = mid(singular_points[0], singular_points[1])
    return estimated_position


# TODO docstrings, typing, testing


def multiple_two_int_handler(two_intersection_points: List[List[Any]]) -> List[Any]:
    """Calculates estimated position of hotspots using circle intersections.

    :param two_intersection_points: intersection points of circles intersecting in two places

    :return: estimated position of hotspots
    """
    candidates = []  # list of points that are close enough to the others
    for h in range(2):
        candidate_1 = two_intersection_points[0][h]
        for i in range(len(two_intersection_points) - 1):
            for j in range(2):
                candidate_2 = two_intersection_points[i + 1][j]
                if haversine(candidate_1, candidate_2, unit=m) < tol:
                    candidates.append(mid(candidate_1, candidate_2))
    if len(candidates) > 1:
        estimated_position = mid(candidates[0], candidates[1])
    elif len(candidates) == 1:
        estimated_position = candidates[0]
    elif len(candidates) == 0:
        estimated_position = no_candidate_handler(two_intersection_points)
    return estimated_position


def singular_two_int_handler(
    two_intersection_points: List[List[float]], centres: List[float]
) -> List[float]:
    """Calculates estimated position of hotspots using circle intersections and \
        shortest distance to its furthest hotspot.

    :param two_intersection_points: intersection points of circles intersecting in two places
    :param centers: list of hotspot locations (centres of circles)

    :return: estimated position of hotspots
    """
    # choose ISP with the shortest distance to its furthest hotspot
    candidate_1 = two_intersection_points[0]
    candidate_2 = two_intersection_points[1]

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
    return estimated_position


def no_candidate_handler(two_intersection_points: List[List[Any]]) -> List[Any]:
    """Calculates estimation position for two intersection handling if there are no suitable candidates.

    :param two_intersection_points: list intersrection points

    :return: estimated position of hotspots
    """
    all_intersects: List[Tuple[float, float]] = sum(two_intersection_points, [])
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
    estimated_position = mid(first_point, second_point)
    return estimated_position
