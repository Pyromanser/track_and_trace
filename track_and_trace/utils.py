from decimal import Decimal
from functools import lru_cache
from typing import Optional

import requests

from django.conf import settings
from cache_memoize import cache_memoize


@lru_cache
def get_coordinates(zip_code: str, country_code: str) -> Optional[tuple[Decimal, Decimal]]:
    url = settings.OPEN_WEATHER_GEOCODE_API_URL.format(
        zip_code=zip_code, country_code=country_code, api_key=settings.OPEN_WEATHER_MAP_API_KEY
    )
    response = requests.get(url)
    if response.status_code != 200:
        return None

    response = response.json()
    return Decimal(response['lat']), Decimal(response['lon'])

@lru_cache
@cache_memoize(60 * 2)
def get_weather(lat: Decimal, lon: Decimal) -> Optional[dict]:
    url = settings.OPEN_WEATHER_API_URL.format(lat=lat, lon=lon, api_key=settings.OPEN_WEATHER_MAP_API_KEY)
    response = requests.get(url)
    if response.status_code != 200:
        return None

    return response.json()
