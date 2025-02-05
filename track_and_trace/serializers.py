from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from track_and_trace.models import Address, Carrier, Shipment, Product, Article


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "street", "city", "zip_code", "country"]


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "SKU"]


class ArticleSerializer(serializers.ModelSerializer):
    article = ProductSerializer()

    class Meta:
        model = Article
        fields = ["id", "article", "article_quantity"]


class ShipmentSerializer(serializers.ModelSerializer):
    carrier = CarrierSerializer()
    sender_address = AddressSerializer()
    receiver_address = AddressSerializer()
    articles = ArticleSerializer(many=True)
    weather = serializers.SerializerMethodField(read_only=True, default={})

    class Meta:
        model = Shipment
        fields = [
            "id",
            "tracking_number",
            "carrier",
            "sender_address",
            "receiver_address",
            "status",
            "articles",
            "weather",
        ]

    @transaction.atomic
    def create(self, validated_data):
        carrier_data = validated_data.pop("carrier")
        sender_address_data = validated_data.pop("sender_address")
        receiver_address_data = validated_data.pop("receiver_address")
        articles_data = validated_data.pop("articles")

        carrier = Carrier.objects.get_or_create(**carrier_data)[0]
        sender_address = Address.objects.get_or_create(**sender_address_data)[0]
        receiver_address = Address.objects.get_or_create(**receiver_address_data)[0]

        shipment = Shipment.objects.create(
            carrier=carrier,
            sender_address=sender_address,
            receiver_address=receiver_address,
            **validated_data,
        )

        for article_data in articles_data:
            product_data = article_data.pop("article")
            article = Product.objects.get_or_create(**product_data)[0]
            Article.objects.create(shipment=shipment, article=article, **article_data)

        return shipment

    @extend_schema_field(serializers.DictField)
    def get_weather(self, obj):
        return obj.weather
