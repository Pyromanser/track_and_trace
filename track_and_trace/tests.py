from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.cache import cache

from track_and_trace.factories import ShipmentFactory


class ShipmentTestCase(APITestCase):
    def setUp(self):
        with patch('track_and_trace.models.Shipment._update_weather'):
            self.shipment_1 = ShipmentFactory()
            self.shipment_2 = ShipmentFactory()

        self.list_url = reverse('track_and_trace:shipment-list')
        self.detail_url = reverse('track_and_trace:shipment-detail', kwargs={'pk': self.shipment_1.pk})

    def tearDown(self):
        cache.clear()

    @patch('track_and_trace.utils.requests.get')
    def test_list_shipments(self, mock_get):
        mock_get.side_effect = [
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'lat': '40.7128', 'lon': '-74.0060'}}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'weather': 'rain'}}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'lat': '20.6355', 'lon': '27.1401'}}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'weather': 'sunny'}}),
        ]

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['weather'], {'weather': 'rain'})
        self.assertEqual(response.data['results'][1]['weather'], {'weather': 'sunny'})

    @patch('track_and_trace.utils.requests.get')
    def test_detail_shipments(self, mock_get):
        mock_get.side_effect = [
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'lat': '40.7128', 'lon': '-74.0060'}}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: {'weather': 'sunny'}}),
        ]

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weather'], {'weather': 'sunny'})
