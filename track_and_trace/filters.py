from django_filters import rest_framework as filters

from track_and_trace.models import Shipment


class ShipmentFilterSet(filters.FilterSet):
    carrier = filters.CharFilter(field_name="carrier__name")
    sender_country = filters.CharFilter(field_name="sender_address__country")
    sender_zip_code = filters.CharFilter(field_name="sender_address__zip_code")
    sender_city = filters.CharFilter(field_name="sender_address__city")
    receiver_country = filters.CharFilter(field_name="receiver_address__country")
    receiver_zip_code = filters.CharFilter(field_name="receiver_address__zip_code")
    receiver_city = filters.CharFilter(field_name="receiver_address__city")

    class Meta:
        model = Shipment
        fields = ["status"]
