from django.core.exceptions import ObjectDoesNotExist

import math
from math import sin, cos, sqrt, atan2, radians
from subscriber_profile.models import SubscriberProfile
from restaurant.models import PendingRestaurant, Restaurant

from operator import itemgetter
import ast

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


def get_nearby_restaurants(user_id, role):
    """ Retrieves the 5 nearest approved restaurants
    in proximity to the GEO_location of the sduser given
    the user_id and their role

    :param user_id: the id of the sduser
    :type user_id: int
    :param role: the sduser's role (BU or RO)
    :type role: str
    :raises ObjectDoesNotExist: if the Subscriber or PendingRestaurnat associated
        with the given user_id does not exist
    :return: list of dict objects, each one containing the restaurant's id
        and distance from the sduser, in ascending order
    :rtype: list of dict
    """
    user = None
    if role == 'BU':
        user = SubscriberProfile.objects.filter(
            user_id=user_id).first()
    else:
        user = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()

    if not user:
        raise ObjectDoesNotExist("The user with the given user_id: "+ user_id +" does not exist")

    user_location = ast.literal_eval(user.GEO_location)
    nearest = []
    restaurants = list(Restaurant.objects.all())
    for restaurant in restaurants:
        if role == 'RO' and restaurant._id == user._id:
            continue
        restaurant_location = ast.literal_eval(restaurant.GEO_location)
        distance = calculate_distance(user_location, restaurant_location)
        nearest.append(
            {"restaurant": str(restaurant._id), "distance": distance})

    nearest = sorted(nearest, key=itemgetter("distance"))
    if (len(nearest) > 5):
        nearest = nearest[:5]
    return nearest