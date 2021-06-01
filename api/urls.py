from django.db.models import base
from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'country', views.CountryView, basename="countries")
router.register(r'state', views.StateView, basename="states")
router.register(r'address', views.AddressView, basename="addresses")


urlpatterns = [
    path('api/', include(router.urls))
]
