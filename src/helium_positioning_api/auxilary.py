from math import sin, cos, sqrt, radians, degrees, atan2
from utm import from_latlon, to_latlon

def midpoint(point_1, point_2):
    """function returning the midpoint latitude and longitude between two hotspots"""
    point_1.load_location()
    point_2.load_location()
    
    # Conversion to radians
    lat1 = radians(point_1.lat)
    lon1 = radians(point_1.long)
    lat2 = radians(point_2.lat)
    lon2 = radians(point_2.long)

    bx = cos(lat2) * cos(lon2 - lon1)
    by = cos(lat2) * sin(lon2 - lon1)
    lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + bx) * (cos(lat1) + bx) + by**2))
    lon3 = lon1 + atan2(by, cos(lat1) + bx)

    return (degrees(lat3), degrees(lon3))


def circle_intersect_plane(lat_0, long_0, radius_0, lat_1, long_1, radius_1):
    """function returning intersection points of two circles in the plane"""

    # calculating distance of the circle's centres
    d = sqrt((lat_1 - lat_0) ** 2 + (long_1 - long_0) ** 2)

    # checking for intersections with said distance
    if d > radius_0 + radius_1:             # non intersecting, returning midpoint
        (lat_3, long_3) = ((lat_0 + lat_1) / 2, (long_0 + long_1) / 2)
        return (lat_3, long_3), (lat_3, long_3)
    if d < abs(radius_0 - radius_1):        # one circle within other, returning midpoint
        # print("one within  other")
        (lat_3, long_3) = ((lat_0 + lat_1) / 2, (long_0 + long_1) / 2)
        return (lat_3, long_3), (lat_3, long_3)

    if d == 0 and radius_0 == radius_1:     # coincident circles
        return None

    # a is the line from the first circle's centre to the
    # line going through both intersections should they exist
    a = (radius_0 ** 2 - radius_1 ** 2 + d ** 2) / (2 * d)

    # h distance of the intersection points to the line going through the circles' centers
    h = sqrt(radius_0 ** 2 - a ** 2)

    lat_2 = lat_0 + a * (lat_1 - lat_0) / d
    long_2 = long_0 + a * (long_1 - long_0) / d
    lat_3 = lat_2 + h * (long_1 - long_0) / d
    long_3 = long_2 - h * (lat_1 - lat_0) / d

    lat_4 = lat_2 - h * (long_1 - long_0) / d
    long_4 = long_2 + h * (lat_1 - lat_0) / d

    return (lat_3, long_3), (lat_4, long_4)

def circle_intersect(latlon0, radius_0, latlon1, radius_1, factor):
    """function performing circle intersection"""
    
    # conversion lat/lon -> UTM coordinates
    lat_0, long_0, zone, letter = from_latlon(latlon0[0], latlon0[1])
    lat_1, long_1, _, _ = from_latlon(latlon1[0], latlon1[1], force_zone_number=zone)

    # calculating intersectin in UTM
    a_utm, b_utm = circle_intersect_plane(lat_0, long_0, radius_0, lat_1, long_1, radius_1, factor)

    # conversion UTM -> lat/lon
    a = to_latlon(a_utm[0], a_utm[1], zone, letter)
    b = to_latlon(b_utm[0], b_utm[1], zone, letter)

    return a, b