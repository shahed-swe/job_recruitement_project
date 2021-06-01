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
    country = CountrySerializer(many=False)
    class Meta:
        model = State
        fields = '__all__'

    def create(self, validate_data):
        new_validate_data = {}
        d1 = Dictionary()
        new_validate_data = d1.dictBack(validate_data)
        country,_ = Country.objects.get_or_create(
            name = new_validate_data.get('name'),
            latitude = new_validate_data.get('latitude'),
            longitude = new_validate_data.get('longitude'),
            code = new_validate_data.get('code')
        )
        state,_ = State.objects.get_or_create(
            country = country,
            name = validate_data['name']
        )
        return state



class AddressSerializer(serializers.ModelSerializer):
    state = StateSerializer(many=False)

    class Meta:
        model = Address
        fields = '__all__'


    def create(self, validate_data):
        outer_dictionary = {}
        d1 = Dictionary()
        outer_dictionary = d1.dictBack(validate_data)
        insider_dictionary = {}
        d2 = Dictionary()
        insider_dictionary = d2.dictBack(outer_dictionary)

        country,_ = Country.objects.get_or_create(
            name = insider_dictionary.get('name'),
            latitude = insider_dictionary.get('latitude'),
            longitude = insider_dictionary.get('longitude'),
            code = insider_dictionary.get('code')
        )

        state, _ = State.objects.get_or_create(
            country = country,
            name= outer_dictionary.get('name')
        )

        address,_ = Address.objects.get_or_create(
            state = state,
            name = validate_data['name'],
            house_number = validate_data['house_number'],
            road_number = validate_data['road_number']
        )

        return address



