import pycountry

from django.db import models
from django.utils.functional import cached_property


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    lat = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    lon = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.zip_code} {self.city}, {self.country}"

    @cached_property
    def country_code(self):
        return pycountry.countries.get(name=self.country).alpha_2

class Carrier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shipment(models.Model):
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
