from django.test import client
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import *
from django.urls import reverse
from django.urls.base import clear_script_prefix
from rest_framework import status
from rest_framework.test import APITestCase

import pytest



class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'email':'test@gmail.com',
            'first_name':'test',
            'last_name':'last',
            'password':'newpass@123',
            're_password':'newpass@123',
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="newpass@123")


    def test_login(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'newpass@123'
        }
        response = self.client.post('/auth/jwt/create/',data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class CountryInput(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com",password="newpass@123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token.access_token}")


    def test_country_insert_bast_case(self):
        data1 = {"name":"bangladesh","latitude":"23.2345","longitude":"56.23234","code":"880"}
        response = self.client.post('/api/country/', data1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_country_worst_case(self):
        # each and every filed is required and that's why we are fetching error in here
        data2 = {"name":"india","latitude":23.556,"longitude":45.5656}
        response = self.client.post('/api/country/', data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CountryFIlter(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com", password="newpass@123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token.access_token}")
        data1 = {"name": "bangladesh", "latitude": "23.2345","longitude": "56.23234", "code": "880"}
        data2 = {"name": "india", "latitude": 23.556, "longitude": 45.5656,"code":"91"}
        self.client.post('/api/country/',data1)
        self.client.post('/api/country/',data2)

    def test_search_country(self):
        data = {"name":"bangladesh"}
        resp = self.client.get(f'/api/country/?name={data.get("name")}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_search_country_again(self):
        data = {"code":"880"}
        resp = self.client.get('/api/country/?code={data.get("code")}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class StateInput(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com", password="newpass@123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token.access_token}")
        self.country = {
            "id":"3",
            "name": "bangladesh",
            "latitude": "23.2345",
            "longitude": "56.23234",
            "code": "880"
        }
        self.client.post('/api/country/', self.country)


    def test_state_insert_best_case(self):
        data = {
            "country": {
                "name": "India",
                "latitude": 43.5768,
                "longitude": 45.345676,
                "code": "91"
            },
            "name": "Delhi"
            
        }
        resp = self.client.post('/api/state/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_state_insert_worst_case(self):
        data = {
            "country": {
                "name": "India",
                "latitude": 43.5768,
                "longitude": 45.345676,
                "code": None
            },
            "name": "Delhi"

        }
        resp = self.client.post('/api/state/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class AddressInput(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com", password="newpass@123")
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token.access_token}")
        self.state = {
            "country": {
                "name": "India",
                "latitude": 43.5768,
                "longitude": 45.345676,
                "code": "91"
            },
            "name": "Delhi"
        }
        self.client.post('/api/state/', self.state, format='json')


    def test_state_insert_best_case(self):
        data = {
            "state": {
                "country": {
                    "name": "India",
                    "latitude": 43.5768,
                    "longitude": 45.345676,
                    "code": "91"
                },
                "name": "Delhi"
            },
            "name": "Baridhara",
            "house_number": "1256",
            "road_number": 950
            
        }
        resp = self.client.post('/api/address/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_state_insert_worst_case(self):
        data = {
            "state": {
                "country": {
                    "name": "India",
                    "latitude": 43.5768,
                    "longitude": 45.345676,
                    "code": "91"
                },
                "name": "Delhi"
            },
            "name": "Baridhara",
            "house_number": None,
            "road_number": 950

        }
        resp = self.client.post('/api/address/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
