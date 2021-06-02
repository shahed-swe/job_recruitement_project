from django.shortcuts import render
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class CountryView(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'code']


class StateView(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class AddressView(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house_number','road_number']


class AddressDetailView(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressDetailSerializer
    http_method_names = ['get']