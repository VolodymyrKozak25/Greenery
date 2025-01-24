from typing import Tuple, Optional
from geopy.geocoders import Nominatim


def get_location(address: str) -> Optional[Tuple[float, float]]:
    """
    Returns the latitude and longitude of a given address
    using geopy's Nominatim geocoder.
    
    :param address: The address to geocode.
    :return: A tuple containing the latitude and longitude
             or None if address could not be geocoded.
    """
    geolocator = Nominatim(user_agent="Tester")
    if location := geolocator.geocode(address):
        return location.latitude, location.longitude


if __name__ == "__main__":
    assert round(get_location("Львів Університетська 1")[0], 5) == 49.84022
    assert round(get_location("Львів Університетська 1")[1], 5) == 24.02229
    assert get_location("Неіснуюча адреса") == None
