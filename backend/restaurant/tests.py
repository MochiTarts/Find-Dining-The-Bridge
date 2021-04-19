from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth import get_user_model

from .models import (
    Restaurant
)
from .views import (
    AllRestaurantList,
    RestaurantView,
    PendingRestaurant,
    RestaurantDraftView,
    RestaurantForApprovalView
)
from utils.model_util import model_to_json, models_to_json

import json

User = get_user_model()


class ApprovedRestaurantTestCases(TestCase):
    """ Tests for restaurants from the Restaurant collection """

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.client = APIClient()
        cls.restaurant_1 = Restaurant.objects.create(name="restaurant 1", email="1@mail.com")
        cls.restaurant_2 = Restaurant.objects.create(name="restaurant 2", email="2@mail.com")
        cls.restaurant_3 = Restaurant.objects.create(name="restaurant 3", email="3@mail.com")

    def test_get_all_restaurants(self):
        """ Test if all approved restaurants are retrieved """
        response = self.client.get('/api/restaurant/all/')
        restaurants = [
            Restaurant.objects.get(email="1@mail.com"),
            Restaurant.objects.get(email="2@mail.com"),
            Restaurant.objects.get(email="3@mail.com")
        ]
        for rest in restaurants:
            rest.restaurant_image_url = ['/']
            rest.payment_methods = ['/']
            rest.offer_options = ['']
            rest.save()
            
        expected = {
            "Restaurants": models_to_json(restaurants)
        }
        self.assertDictEqual(json.loads(response.content), expected)