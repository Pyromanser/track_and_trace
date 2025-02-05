from django.urls import include, path

from rest_framework import routers

from track_and_trace import views

router = routers.DefaultRouter()
router.register(r'shipments', views.ShipmentViewSet)

app_name = 'track_and_trace'
urlpatterns = [
    path('', include(router.urls)),
]