from typing import Optional

from django.db import models
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE
from django_lifecycle.conditions import WhenFieldHasChanged

from track_and_trace.utils import get_country_code, get_coordinates, get_weather


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.zip_code} {self.city}, {self.country}"

    @property
    def weather(self) -> Optional[dict]:
        country_code = get_country_code(self.country)
        if not country_code:
            return {}

        coordinates = get_coordinates(self.zip_code, country_code)
        if not coordinates:
            return {}

        lat, lon = coordinates
        return get_weather(lat, lon)

class Carrier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shipment(LifecycleModel):
    class Status(models.TextChoices):
        IN_TRANSIT = 'in-transit', 'In Transit'
        INBOUND_SCAN = 'inbound-scan', 'Inbound Scan'
        DELIVERY = 'delivery', 'Delivery'
        TRANSIT = 'transit', 'Transit'
        SCANNED = 'scanned', 'Scanned'

    tracking_number = models.CharField(max_length=20)
    carrier = models.ForeignKey(Carrier, related_name='shipments', on_delete=models.CASCADE)
    sender_address = models.ForeignKey(Address, related_name='sender_shipments', on_delete=models.CASCADE)
    receiver_address = models.ForeignKey(Address, related_name='receiver_shipments', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices)

    def __str__(self):
        return f"{self.tracking_number} - {self.carrier}"

    @property
    def weather(self) -> Optional[dict]:
        return self.receiver_address.weather

    def _update_weather(self):
        return self.weather

    @hook(AFTER_CREATE)
    def on_create(self):
        self._update_weather()

    @hook(AFTER_UPDATE, condition=WhenFieldHasChanged('receiver_address', has_changed=True))
    def on_receiver_address_change(self):
        self._update_weather()

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.SKU})"

class Article(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='articles', on_delete=models.CASCADE)
    article_quantity = models.PositiveSmallIntegerField()
    article = models.ForeignKey(Product, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.article.name}, {self.article_quantity}"
