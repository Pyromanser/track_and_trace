from celery import shared_task
from django.db.models import F

from track_and_trace.models import Shipment
from track_and_trace.utils import get_country_code, get_coordinates, get_weather


@shared_task
def update_weather():
    shipments = (
        Shipment.objects.select_related("receiver_address")
        .values(
            country=F("receiver_address__country"),
            zip_code=F("receiver_address__zip_code"),
        )
        .distinct()
    )
    for shipment in shipments:
        country_code = get_country_code(shipment["country"])
        if not country_code:
            continue

        coordinates = get_coordinates(shipment["zip_code"], country_code)
        if not coordinates:
            continue

        lat, lon = coordinates
        get_weather(lat, lon)
