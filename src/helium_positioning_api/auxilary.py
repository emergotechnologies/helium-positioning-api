"""Helper functions for the positioning API."""
from math import atan2
from math import cos
from math import degrees
from math import radians
from math import sin
from math import sqrt
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Union

from helium_api_wrapper.DataObjects import IntegrationHotspot
from helium_api_wrapper.devices import get_last_integration
from utm import from_latlon
from utm import to_latlon


def get_integration_hotspots(uuid: str) -> List[IntegrationHotspot]:
    """Load hotspots, which interacted with the given device from the last integration event."""
    integration = get_last_integration(uuid)
    if len(integration.hotspots) == 0:
        raise ValueError(f"No hotspots found for device {uuid}")
    return integration.hotspots


def get_midpoint(
    point_1: IntegrationHotspot, point_2: IntegrationHotspot
) -> Iterable[Union[float, float]]:
    """Return the midpoint coordinates between two hotspots.

    :param point_1: first Hotspot
    :param point_2: second Hotspot

    :return: coordinates of midpoint between point_1 and point_2
    """
    # Conversion to radians
    if point_1.lat is not None:
        lat1 = radians(point_1.lat)
    else:
        raise ValueError("Latitude of point_1 is None")
    if point_1.lng is not None:
        lon1 = radians(point_1.lng)
    else:
        raise ValueError("Longitude of point_1 is None")
    if point_2.lat is not None:
        lat2 = radians(point_2.lat)
    else:
        raise ValueError("Latitude of point_2 is None")
    if point_2.lng is not None:
        lon2 = radians(point_2.lng)
    else:
        raise ValueError("Longitude of point_2 is None")

    bx = cos(lat2) * cos(lon2 - lon1)
    by = cos(lat2) * sin(lon2 - lon1)
    lat3 = atan2(
        sin(lat1) + sin(lat2), sqrt((cos(lat1) + bx) * (cos(lat1) + bx) + by**2)
    )
    lon3 = lon1 + atan2(by, cos(lat1) + bx)

    return (degrees(lat3), degrees(lon3))


def circle_intersect_plane(
    lat_0: float,
    long_0: float,
    radius_0: float,
    lat_1: float,
    long_1: float,
    radius_1: float,
) -> Union[Tuple[Tuple[float, float], Tuple[float, float]], Tuple[None, None]]:
    """Return intersection points of two circles in the plane.

    :param lat_0: latitude of first centre
    :param long_0: longitude of first centre
    :param radius_0: radius of first circle
    :param lat_1: latitude of second centre
    :param long_1: longitude of second centre
    :param radius_1: radius of second circle

    :return: coordinates of intersection points
    """
    # calculating distance of the circle's centres
    d = sqrt((lat_1 - lat_0) ** 2 + (long_1 - long_0) ** 2)

    # checking for intersections with said distance
    if d > radius_0 + radius_1:  # non intersecting, returning midpoint
        (lat_3, long_3) = ((lat_0 + lat_1) / 2, (long_0 + long_1) / 2)
        return (lat_3, long_3), (lat_3, long_3)
    if d < abs(radius_0 - radius_1):
        # one circle within other, returning midpoint
        # print("one within  other")
        (lat_3, long_3) = ((lat_0 + lat_1) / 2, (long_0 + long_1) / 2)
        return (lat_3, long_3), (lat_3, long_3)

    if d == 0 and radius_0 == radius_1:  # coincident circles
        return (None, None)

    # a is the line from the first circle's centre to the
    # line going through both intersections should they exist
    a = (radius_0**2 - radius_1**2 + d**2) / (2 * d)

    # h distance of the intersection points to the line
    # going through the circles' centers
    h = sqrt(radius_0**2 - a**2)

    lat_2 = lat_0 + a * (lat_1 - lat_0) / d
    long_2 = long_0 + a * (long_1 - long_0) / d
    lat_3 = lat_2 + h * (long_1 - long_0) / d
    long_3 = long_2 - h * (lat_1 - lat_0) / d

    lat_4 = lat_2 - h * (long_1 - long_0) / d
    long_4 = long_2 + h * (lat_1 - lat_0) / d

    return (lat_3, long_3), (lat_4, long_4)


def circle_intersect(
    latlon0: Union[Tuple[float, float], List[float]],
    radius_0: float,
    latlon1: Union[Tuple[float, float], List[float]],
    radius_1: float,
) -> Union[Tuple[float, float], Tuple[float, float]]:
    """Perform circle intersection.

    :param latlon0: coordinates of first centre
    :param radius_0: radius of first circle
    :param latlon1: coordinates of second centre
    :param radius_1: radius of second circle

    :return: coordinates of intersection points
    """
    # conversion lat/lon -> UTM coordinates
    lat_0, long_0, zone, letter = from_latlon(latlon0[0], latlon0[1])
    lat_1, long_1, _, _ = from_latlon(latlon1[0], latlon1[1], force_zone_number=zone)

    # calculating intersectin in UTM
    a_utm, b_utm = circle_intersect_plane(
        lat_0, long_0, radius_0, lat_1, long_1, radius_1
    )
    # conversion UTM -> lat/lon
    if a_utm is not None:
        a = to_latlon(a_utm[0], a_utm[1], zone, letter)
    else:
        raise ValueError("No intersection found")
    if b_utm is not None:
        b = to_latlon(b_utm[0], b_utm[1], zone, letter)
    else:
        raise ValueError("No intersection found")

    return a, b


def get_centres(
    latitude: List[float],
    longitude: List[float],
    indices: Tuple[int, int, int] = (0, 1, 2),
) -> Tuple[List[float], List[float], List[float], Tuple[int, int, int]]:
    """Return latitude/longitude of hotspots from list of indices.

    :param latitude: latitudes
    :type latitude: list of latitudes (floats)
    :param longitude: longitudes
    :type longitude: list of longitudes (floats)
    :param indices: indices of hotspots
    :type indices: tuple of three integers

    :return: centres of hotspots with the given indices and the indices
    :rtype: list of latitudes and longitudes in degree and indices as int

    """
    centre_0 = [latitude[indices[0]], longitude[indices[0]]]
    centre_1 = [latitude[indices[1]], longitude[indices[1]]]
    centre_2 = [latitude[indices[2]], longitude[indices[2]]]

    return centre_0, centre_1, centre_2, indices


def flatten_intersect_lists(input_list: List[Iterable[float]]) -> List[float]:
    """Flattens lists.

    :param input_list: List of lists
    :type input_list: list of lists

    :return: list
    :rtype: list
    """
    flattened_list = []
    if len(input_list) != 0:
        if isinstance(input_list[0], list):
            flattened_list = [point for sublist in input_list for point in sublist]
    return flattened_list


def mid(
    point_1: Union[List[float], Tuple[float, float]],
    point_2: Union[List[float], Tuple[float, float]],
) -> Tuple[float, float]:
    """Return midpoint of two points given in lat/long coordinates.

    :param point_1: first point
    :param point_2: second point

    :return: coordinates of midpoint between point_1 and point_2
    """
    # Input values as degrees

    # Convert to radians
    lat1 = radians(point_1[0])
    lon1 = radians(point_1[1])
    lat2 = radians(point_2[0])
    lon2 = radians(point_2[1])

    bx = cos(lat2) * cos(lon2 - lon1)
    by = cos(lat2) * sin(lon2 - lon1)
    lat3 = atan2(
        sin(lat1) + sin(lat2), sqrt((cos(lat1) + bx) * (cos(lat1) + bx) + by**2)
    )
    lon3 = lon1 + atan2(by, cos(lat1) + bx)

    return (degrees(lat3), degrees(lon3))
