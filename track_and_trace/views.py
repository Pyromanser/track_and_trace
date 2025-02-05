from django.db.models import Prefetch
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from track_and_trace.models import Address, Carrier, Shipment, Product, Article
from track_and_trace.serializers import AddressSerializer, CarrierSerializer, ShipmentSerializer, ProductSerializer, ArticleSerializer
from track_and_trace.filters import ShipmentFilterSet


@extend_schema_view(
    list=extend_schema(
        description='List all shipments',
    ),
    retrieve=extend_schema(
        description='Retrieve a shipment',
    ),
    create=extend_schema(
        description='Create a shipment',
    ),
    update=extend_schema(
        description='Update a shipment',
    ),
    partial_update=extend_schema(
        description='Partially update a shipment',
    ),
    destroy=extend_schema(
        description='Delete a shipment',
    ),
)
class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.none()
    serializer_class = ShipmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ShipmentFilterSet

    def get_queryset(self):
        return Shipment.objects.select_related(
            'carrier', 'sender_address', 'receiver_address'
        ).prefetch_related(
            Prefetch('articles', queryset=Article.objects.select_related('article'))
        )