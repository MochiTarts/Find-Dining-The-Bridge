import math
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(user_coord, restr_coord):
    """ Calculates the distance between two coordinates

    :param: user_coord: latitude and longitude of the sduser's GEO_location
    :param: restr_coord: latitude and longitude of the restaurant's GEO_location
    :return: the distance (in km) between the 2 coordinates
    """
    radius = 6373

    user_lat = radians(user_coord.get('lat'))
    user_lng = radians(user_coord.get('lng'))
    restr_lat = radians(restr_coord.get('lat'))
    restr_lng = radians(restr_coord.get('lng'))

    lat_distance = restr_lat - user_lat
    lng_distance = restr_lng - user_lng

    a = sin(lat_distance/2)**2 + cos(user_lat)*cos(restr_lat)*sin(lng_distance/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))

    distance = radius * c
    return distance