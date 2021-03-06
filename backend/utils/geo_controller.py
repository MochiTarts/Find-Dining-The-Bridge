from django.conf import settings
from django.core.exceptions import ValidationError

# geolocation library
import googlemaps
import json

client = googlemaps.Client(settings.GEOCODE_API_KEY)


def geocode(address):
    """ Retrieves coordinates from a given address

    :params address: address to be geocoded
    :type address: str
    :raises ValidationError: for no results or multiple results
    :return: longitude and latitude of an address
    :rtype: dict
    """
    results = client.geocode(address)
    if len(results) == 0:
        raise ValidationError(
            message='No results from the given address: ' + address,
            code='location_not_exist')
    else:
        return results[0]['geometry']['location']


def reverse_geocode(coordinates):
    """ Retrieves formatted address from coordinates

    :param coordinates: lat, lng of a location
    :type coordinates: dict
    :raises ValidationError: if no results come from the
        given coordinates
    :return: the formatted address
    :rtype: str
    """
    address = client.reverse_geocode(coordinates)
    if len(address) == 0:
        raise ValidationError("No results from given coordinates",
        code='address_not_found')
    return address[0]['formatted_address']


def in_scarborough(coord):
    """
    param: a tuple containing the geographic coordinates
    example: (43.7825084, -79.1853174)
    return: boolean indicating whether the given
    geographic coordinates is within scarborough
    """
    try:
        #results = client.reverse_geocode(latlng=coord, result_type='sublocality')
        results = client.reverse_geocode(latlng=coord)
    except Exception as e:
        results = []
    finally:
        if len(results) == 0:
            return False
        elif len(results) == 1:
            addr = results[0]
            #components = addr['address_components']
            formatted_address = addr['formatted_address']
            return 'Scarborough' in formatted_address
        else:
            for addr in results:
                formatted_address = addr['formatted_address']
                return 'Scarborough' in formatted_address
