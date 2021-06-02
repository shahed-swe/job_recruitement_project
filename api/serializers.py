from django.test.client import conditional_content_removal
from .utils import Dictionary
from django.db.models import fields
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','first_name','last_name','password')



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    countryof = CountrySerializer(many=True, read_only=True)
    class Meta:
        model = State
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    stateof = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Address
        fields = '__all__'



class AddressDetailSerializer(serializers.ModelSerializer):
    stateof = StateSerializer(many=False, read_only=True)

    class Meta:
        model = Address
        fields = '__all__'




