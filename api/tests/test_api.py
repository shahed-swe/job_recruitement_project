from _pytest.mark import param
from django.contrib.auth.base_user import BaseUserManager
from django.db import reset_queries
from django.http import response
import pytest
import json
# from django.test import Client
from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


@pytest.mark.django_db
class BasicCountryTestCase(APITestCase):
    def setUp(self)->None:
        self.country_url = reverse('countries-list')
        self.user = User.objects.create_user(email="test@gmail.com",first_name="test", last_name="last",password="newpass@123")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.token.access_token}")

    def tearDown(self) -> None:
        pass


class TestCountryDemo(BasicCountryTestCase):

    def test_zero_country_list(self)->None:
        response = self.client.get(self.country_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

    def test_one_country_exist(self)->None:
        country = Country.objects.create(name="Bangladesh",latitude="45.1241341", longitude="47.1234",code="880")
        response = self.client.get(self.country_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_every_columns_needs_to_register(self)->None:
        body = {
            "name":"Bangladesh",
            "latitude":"56.64567",
            "longitude":"45.67",
            "code":"880"
        }
        response = self.client.post(self.country_url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content),{
            "id":1,
            "name":"Bangladesh",
            "latitude":56.64567,
            "longitude":45.67,
            "code":"880"}
            )


    def test_every_columns_needs_to_register_two(self)->None:
        body = {
            "name":"India",
            "latitude":"67.23454",
            "longitude":"123.2345",
            "code": ""
        }
        response = self.client.post(self.country_url, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_columns_to_update_all(self)->None:
        country = Country.objects.create(name="Bangladesh",latitude="45.1241341", longitude="47.1234",code="880")
        data = {
            "name": "India",
            "latitude":56.6768,
            "longitude":78.3245,
            "code":"91"
        }
        response = self.client.put(self.country_url+f"{country.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),{
            "id":country.pk,
            "name": "India",
            "latitude":56.6768,
            "longitude":78.3245,
            "code":"91"
        })

    def test_update_individual_column(self)->None:
        country = Country.objects.create(name="India",latitude="45.1241341", longitude="47.1234",code="880")
        data = {
            "name":"Bangladesh",
        }
        response = self.client.patch(self.country_url+f"{country.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),{"id":country.pk,"name":"Bangladesh","latitude":45.1241341,"longitude":47.1234,"code":"880"})

    def test_delete_data(self)->None:
        country = Country.objects.create(name="India",latitude="45.1241341", longitude="47.1234",code="880")
        response = self.client.delete(self.country_url+f"{country.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(response.content)



@pytest.mark.django_db
class BasicStateTestCase(APITestCase):
    def setUp(self)->None:
        self.state_url = reverse('states-list')
        self.user = User.objects.create_user(email="testmain@gmail.com", first_name="test", last_name="last",password="hello@123")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.token.access_token}")
        self.country = Country.objects.create(name="Bangladesh",latitude="45.1241341", longitude="47.1234",code="880")
    
    def tearDown(self) -> None:
        pass

class TestStateDemo(BasicStateTestCase):
    def test_zero_state_list(self)->None:
        response = self.client.get(self.state_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

    def test_one_state_exists(self)->None:
        state = State.objects.create(country=self.country, name="Rajshahi")
        response = self.client.get(self.state_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),[{
            "id":1,
            "country":{
                    "id":1,
                    "name":"Bangladesh",
                    "latitude":45.1241341,
                    "longitude":47.1234,
                    "code":"880"
                },
                "name":"Rajshahi"
        }])