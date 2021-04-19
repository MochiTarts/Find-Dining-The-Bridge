from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth import get_user_model

from .models import (
    Restaurant,
    PendingRestaurant
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

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.restaurant_1 = Restaurant.objects.create(name="restaurant 1", email="1@mail.com")
        self.restaurant_2 = Restaurant.objects.create(name="restaurant 2", email="2@mail.com")
        self.restaurant_3 = Restaurant.objects.create(name="restaurant 3", email="3@mail.com")

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

    def test_get_approved_restaurant(self):
        """ Test if approved restaurant is retrieved by _id """
        _id = Restaurant.objects.get(email="1@mail.com")._id
        response = self.client.get('/api/restaurant/approved/'+str(_id)+'/')

        restaurant = Restaurant.objects.get(email="1@mail.com")
        restaurant.restaurant_image_url = ['/']
        restaurant.payment_methods = ['/']
        restaurant.offer_options = ['']
        restaurant.save()

        expected = model_to_json(restaurant)
        self.assertDictEqual(json.loads(response.content), expected)


class DraftRestaurantTestCases(TestCase):
    """ Tests for pending restaurants marked as drafts """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant_draft = PendingRestaurant.objects.create(name="test draft", email="draft@mail.com")

    def test_insert_restaurant_draft(self):
        """ Tests to see if restaurant draft is inserted correctly """
        restaurant_draft = {
            "name": "Test Restaurant",
            "address": "300 Borough Dr",
            "postalCode": "M1C 3A4",
            "email": "bob@mail.com",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"]
        }
        response = self.client.post('/api/restaurant/draft/', restaurant_draft, format='json')
        self.assertTrue(PendingRestaurant.objects.filter(
            name="Test Restaurant",
            address="300 Borough Dr",
            postalCode="M1C 3A4",
            email="bob@mail.com",
            owner_first_name=["Bob"],
            owner_last_name=["Smith"],
            status="In_Progress").exists())