from django.contrib.auth.base_user import BaseUserManager
import pytest
from unittest import TestCase
import json
# from django.test import Client
from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import *
from rest_framework_simplejwt.tokens import RefreshToken



@pytest.mark.django_db
class BasicCountryTestCase(APITestCase):
    def setUp(self)->None:
        self.country_url = reverse('countries-list')
        self.user = User.objects.create_user(email="test@gmail.com",first_name="test", last_name="last",password="newpass@123")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.token.access_token}")

    def tearDown(self) -> None:
        pass


class TestDemo(BasicCountryTestCase):

    def test_zero_country_list(self)->None:
        response = self.client.get(self.country_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_country_exist(self)->None:
        country = Country.objects.create(name="Bangladesh",latitude="45.1241341", longitude="47.1234",code="880")
        response = self.client.get(self.country_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)

    def test_every_columns_needs_to_register(self)->None:
        body = {
            "name":"Bangladesh",
            "latitude":"56.64567",
            "longitude":"45.67",
            "code":"880"
        }
        response = self.client.post(self.country_url, body)
        self.assertEqual(response.status_code, 201)
