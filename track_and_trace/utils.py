from decimal import Decimal
from functools import lru_cache
from typing import Optional

import logging
import pycountry
import requests

from django.conf import settings
from cache_memoize import cache_memoize


logger = logging.getLogger(__name__)


@lru_cache
def get_country_code(country_name: str) -> Optional[str]:
    logger.debug(f"Getting country code for {country_name}")
    country = pycountry.countries.get(name=country_name)
    if country is None:
        logger.error(f"Failed to get country code for {country_name}")
        return None
    return country.alpha_2


@lru_cache
def get_coordinates(
    zip_code: str, country_code: str
) -> Optional[tuple[Decimal, Decimal]]:
    logger.debug(f"Getting coordinates for {zip_code}, {country_code}")
    url = settings.OPEN_WEATHER_GEOCODE_API_URL.format(
        zip_code=zip_code,
        country_code=country_code,
        api_key=settings.OPEN_WEATHER_MAP_API_KEY,
    )
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to get coordinates for {zip_code}, {country_code}")
        return None

    response = response.json()
    return Decimal(response["lat"]), Decimal(response["lon"])


@cache_memoize(60 * 60 * 2)
def get_weather(lat: Decimal, lon: Decimal) -> Optional[dict]:
    logger.debug(f"Getting weather for {lat}, {lon}")
    url = settings.OPEN_WEATHER_API_URL.format(
        lat=lat, lon=lon, api_key=settings.OPEN_WEATHER_MAP_API_KEY
    )
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to get weather for {lat}, {lon}")
        return None

    return response.json()
