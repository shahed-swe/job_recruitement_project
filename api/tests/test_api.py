import pytest
from unittest import TestCase

from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestDemo(TestCase):

    
    def test_zero_country_list(self)->None:
        client = Client()
        country_url = reverse('countries-list')
        response = client.get(country_url)
        self.assertEqual(response.status_code, 200)
