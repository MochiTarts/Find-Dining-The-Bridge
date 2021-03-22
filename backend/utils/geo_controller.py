from django.conf import settings

# geolocation library
import googlemaps
import json

client = googlemaps.Client(settings.GEOCODE_API_KEY)


def geocode(address):
    """
    :params-address: address to be geocoded
    return longitude and latitude of an address
    raises Value error for no results or multiple results
    """
    results = client.geocode(address)
    if len(results) == 0:
        raise ValueError('No results')
    elif len(results) == 1:
        return results[0]['geometry']['location']
    else:
        raise ValueError('Ambiguous query')

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
