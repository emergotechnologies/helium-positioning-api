from math import sin, cos, sqrt, radians, degrees, atan2


def midpoint(point_1, point_2):
    """function returning the midpoint latitude and longitude between two hotspots"""
    point_1.load_locatoin()
    point_2.loat_location()
    
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
