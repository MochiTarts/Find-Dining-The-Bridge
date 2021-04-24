from django.test import TestCase
from django.contrib.auth import get_user_model

from utils.model_util import model_to_json, models_to_json
from restaurant.enum import Status, Prices, Categories, Payment
from restaurant.models import (
    Restaurant,
    PendingRestaurant,
    RestaurantPost
)
from restaurant.views import (
    AllRestaurantList,
    RestaurantView,
    PendingRestaurant,
    RestaurantDraftView,
    RestaurantForApprovalView
)

from rest_framework.test import APIClient, force_authenticate

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

        expected = model_to_json(restaurant)
        self.assertDictEqual(json.loads(response.content), expected)


class DraftRestaurantTestCases(TestCase):
    """ Tests for pending restaurants marked as drafts """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant_draft = PendingRestaurant.objects.create(
            name="test draft",
            owner_user_id=self.ro.id,
            address="431 Kwapis BLVD",
            postalCode="L3X 3H5",
            email="draft@mail.com"
        )

    def test_insert_restaurant_draft_valid(self):
        """ Tests to see if restaurant draft is inserted correctly """
        restaurant_draft = {
            "name": "Test Restaurant",
            "address": "300 Borough Str",
            "postalCode": "M1P 4P5",
            "email": "bob@mail.com",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"],
            "phone": 4166688966,
            "phone_ext": 1200
        }
        response = self.client.post('/api/restaurant/draft/', restaurant_draft, format='json')
        self.assertTrue(PendingRestaurant.objects.filter(
            name="Test Restaurant",
            years=1,
            address="300 Borough Str",
            postalCode="M1P 4P5",
            email="bob@mail.com",
            owner_first_name=["Bob"],
            owner_last_name=["Smith"],
            phone=4166688966,
            phone_ext=1200,
            status="In_Progress").exists())

    def test_insert_restaurant_draft_invalid(self):
        """ Tests to see if proper error message is returned from invalid inputs """
        restaurant_draft = {
            "name": "Test Restaurant",
            "address": "",
            "postalCode": "M1M 1M0",
            "email": "bob@mail.com",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"],
            "phone": 4166688966,
            "phone_ext": 1200
        }
        response = self.client.post('/api/restaurant/draft/', restaurant_draft, format='json')
        expected = {'status': 400, 'code': 'bad_request', 'detail': {'Invalid': ['address', 'postalCode']}}
        print(json.loads(response.content))
        self.assertFalse(PendingRestaurant.objects.filter(
            name="Test Restaurant",
            years=1,
            address="",
            postalCode="M1M 1M0",
            email="bob@mail.com",
            owner_first_name=["Bob"],
            owner_last_name=["Smith"],
            phone=4166688966,
            phone_ext=1200,
            status="In_Progress").exists())
        self.assertTrue(json.loads(response.content), expected)

    def test_edit_restaurant_draft_valid(self):
        """ Tests to see if restaurant draft is updated correctly """
        edit_draft = {
            "name": "test draft 2",
            "address": "1265 Military Trail",
            "postalCode": "M1C 1A4",
            "email": "draft@mail.com",
            "owner_first_name": ["Jenny"],
            "owner_last_name": ["Yu"],
            "phone": 4166688966,
            "phone_ext": 1200
        }
        response = self.client.put('/api/restaurant/draft/', edit_draft, format='json')
        restaurant = PendingRestaurant.objects.filter(owner_user_id=self.ro.id).first()
        self.assertTrue(
            restaurant.name == "test draft 2" and restaurant.years == 1 and restaurant.address == "1265 Military Trail"
            and restaurant.postalCode == "M1C 1A4" and restaurant.owner_first_name == ["Jenny"]
            and restaurant.owner_last_name == ["Yu"] and restaurant.phone == 4166688966
            and restaurant.phone_ext == 1200)


class RestaurantApprovalTestCases(TestCase):
    """ Tests for pending restaurants marked for waiting on admin approval """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant = PendingRestaurant.objects.create(
            name="Restaurant For Approval",
            owner_user_id=self.ro.id
        )

    def test_insert_restaurant_submission_valid(self):
        """ Test if restaurant for approval is inserted correctly """
        restaurant_submission = {
            "name": "Test Restaurant",
            "years": 1,
            "address": "300 Borough Dr",
            "postalCode": "M1C 3A4",
            "phone": 1234567890,
            "email": "bob@mail.com",
            "pricepoint": Prices.LOW.name,
            "offer_options": ["pick-up", "delivery"],
            "bio": "Story...",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"],
            "open_hours": "9-5",
            "payment_methods": [Payment.Credit.name, Payment.Debit.name],
            "phone_ext": 1200
        }
        response = self.client.put('/api/restaurant/submit/', restaurant_submission, format='json')
        self.assertTrue(PendingRestaurant.objects.filter(
            name="Test Restaurant",
            years=1,
            address="300 Borough Dr",
            postalCode="M1C 3A4",
            phone=1234567890,
            email="bob@mail.com",
            pricepoint=Prices.LOW.name,
            offer_options=["pick-up", "delivery"],
            bio="Story...",
            owner_first_name=["Bob"],
            owner_last_name=["Smitih"],
            open_hours="9-5",
            payment_methods=[Payment.Credit.name, Payment.Debit.name],
            phone_ext=1200,
            status=Status.Pending.name).exists)

    def test_insert_restaurant_submission_invalid(self):
        """ Test if proper error message is returned from invalid inputs """
        restaurant_submission = {
            "name": "Test Restaurant",
            "years": 1,
            "address": "4100 Somewhere Str",
            "postalCode": "M1C 000",
            "phone": 1234567890,
            "email": "bob@mail.com",
            "pricepoint": Prices.LOW.name,
            "offer_options": ["pick-up", "delivery"],
            "bio": "Story...",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"],
            "open_hours": "9-5",
            "payment_methods": [Payment.Credit.name, Payment.Debit.name],
            "phone_ext": 1200
        }
        response = self.client.put('/api/restaurant/submit/', restaurant_submission, format='json')
        expected = {'status': 400, 'code': 'bad_request', 'detail': {'Invalid': ['postalCode']}}
        self.assertFalse(PendingRestaurant.objects.filter(
            name="Test Restaurant",
            years=1,
            address="4100 Somewhere Str",
            postalCode="M1C 000",
            phone=1234567890,
            email="bob@mail.com",
            pricepoint=Prices.LOW.name,
            offer_options=["pick-up", "delivery"],
            bio="Story...",
            owner_first_name=["Bob"],
            owner_last_name=["Smitih"],
            open_hours="9-5",
            payment_methods=[Payment.Credit.name, Payment.Debit.name],
            phone_ext=1200,
            status=Status.Pending.name).exists())
        self.assertTrue(json.loads(response.content), expected)

    def test_edit_restaurant_submission_valid(self):
        """ Test if restaurnat for approval is updated correctly """
        edit_submission = {
            "name": "Test Restaurant 2",
            "years": 10,
            "address": "300 Borough Dr",
            "postalCode": "M1C 3A4",
            "phone": 1234567890,
            "email": "bob@mail.com",
            "pricepoint": Prices.LOW.name,
            "offer_options": ["pick-up", "delivery"],
            "bio": "Story...",
            "owner_first_name": ["Bob"],
            "owner_last_name": ["Smith"],
            "open_hours": "9-5",
            "payment_methods": [Payment.Credit.name, Payment.Debit.name],
            "phone_ext": 1200
        }
        response = self.client.put('/api/restaurant/submit/', edit_submission, format='json')
        self.assertTrue(PendingRestaurant.objects.filter(
            name="Test Restaurant 2",
            years=10,
            address="300 Borough Dr",
            postalCode="M1C 3A4",
            phone=1234567890,
            email="bob@mail.com",
            pricepoint=Prices.LOW.name,
            offer_options=["pick-up", "delivery"],
            bio="Story...",
            owner_first_name=["Bob"],
            owner_last_name=["Smitih"],
            open_hours="9-5",
            payment_methods=[Payment.Credit.name, Payment.Debit.name],
            phone_ext=1200,
            status=Status.Pending.name).exists)


class PendingRestaurantTestCases(TestCase):
    """ Tests for retrieving a pending restaurant """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant = PendingRestaurant.objects.create(owner_user_id=self.ro.id)

    def test_get_pending_restaurant(self):
        """ Test if pending restaurant owned by ro is retrieved properly """
        response = self.client.get('/api/restaurant/pending/')
        restaurant = PendingRestaurant.objects.get(owner_user_id=self.ro.id)
        restaurant.restaurant_image_url = ['/']
        restaurant.payment_methods = ['/']
        restaurant.offer_options = ['']

        expected = model_to_json(restaurant)
        self.assertDictEqual(json.loads(response.content), expected)


class RestaurantPostTestCases(TestCase):
    """ Tests for restaurant posts """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant = PendingRestaurant.objects.create(owner_user_id=self.ro.id)
        self.post_1 = RestaurantPost.objects.create(
            restaurant_id=str(self.restaurant._id),
            content="Test restaurant post 1",
            owner_user_id=self.ro.id
        )
        self.post_2 = RestaurantPost.objects.create(
            restaurant_id=str(self.restaurant._id),
            content="Test restaurant post 2",
            owner_user_id=self.ro.id
        )

    def test_insert_post(self):
        """ Test if restaurant post is inserted correctly """
        post = {
            "restaurant_id": str(self.restaurant._id),
            "content": "Example restaurant post"
        }
        response = self.client.post('/api/restaurant/post/', post, format='json')
        self.assertTrue(RestaurantPost.objects.filter(
            restaurant_id=str(self.restaurant._id),
            content="Example restaurant post"
        ).exists())

    def test_get_post(self):
        """ Test if restaurant posts are retrieved correctly """
        response = self.client.get('/api/restaurant/post/')
        actual = json.loads(response.content)
        for post in actual['Posts']:
            post.pop('Timestamp')
        posts = [
            model_to_json(RestaurantPost.objects.get(content="Test restaurant post 1")),
            model_to_json(RestaurantPost.objects.get(content="Test restaurant post 2"))
        ]

        expected = {"Posts": posts}
        self.assertDictEqual(actual, expected)