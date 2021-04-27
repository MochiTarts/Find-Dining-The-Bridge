from django.test import TestCase
from django.contrib.auth import get_user_model

from utils.model_util import model_to_json, models_to_json
from restaurant.enum import Status, Prices, Categories, Payment
from restaurant.models import (
    Food,
    PendingFood,
    Restaurant,
    PendingRestaurant,
    UserFavRestrs,
    RestaurantPost
)

from rest_framework.test import APIClient, force_authenticate

import json
import ast

User = get_user_model()


class ApprovedFoodTestCases(TestCase):
    """ Tests for food from the Food collection """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant = Restaurant.objects.create(
            name="test",
            owner_user_id=self.ro.id,
            address="431 Kwapis BLVD",
            postalCode="L3X 3H5",
            email="test@mail.com"
        )
        self.dish_1 = Food.objects.create(
            name="dish 1",
            restaurant_id=str(self.restaurant._id),
            category="Specials",
            price="10.50"
        )
        self.dish_2 = Food.objects.create(
            name="dish 2",
            restaurant_id=str(self.restaurant._id),
            category="Specials",
            price="10"   
        )

    def test_get_all_dishes(self):
        """ Test if all dishes from a restaurant is retrieved correctly """
        response = self.client.get('/api/dish/approved/'+str(self.restaurant._id)+'/')
        dishes = [
            model_to_json(Food.objects.get(_id=str(self.dish_1._id))),
            model_to_json(Food.objects.get(_id=str(self.dish_2._id)))
        ]
        expected = {'Dishes': dishes}
        self.assertDictEqual(expected, json.loads(response.content))


class PendingFoodTestCases(TestCase):
    """ Tests for food from the PendingFood collection """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.ro = User.objects.create(username="TestOwner", role="RO")
        self.client.force_authenticate(user=self.ro)
        self.restaurant = PendingRestaurant.objects.create(
            name="test",
            owner_user_id=self.ro.id,
            address="431 Kwapis BLVD",
            postalCode="L3X 3H5",
            email="test@mail.com"
        )
        self.dish_2 = PendingFood.objects.create(
            name="dish 2",
            restaurant_id=str(self.restaurant._id),
            category="Specials",
            price="10"   
        )

    def test_insert_dish_valid(self):
        """ Tests if dish is inserted correctly """
        dish = {
            "name": "dish 1",
            "category": "Specials",
            "specials": "",
            "description": "dish 1 desc",
            "price": "10.50"
        }
        response = self.client.post('/api/dish/pending/', dish, format='json')
        actual = json.loads(response.content)
        self.assertTrue(PendingFood.objects.filter(
            _id=actual['_id'],
            name="dish 1",
            description="dish 1 desc",
            restaurant_id=str(self.restaurant._id),
            category="Specials",
            status=Status.Pending.name
        ).exists())

    def test_get_dishes(self):
        """ Tests if dishes for restaurant owned by user are retrieved correctly """
        response = self.client.get('/api/dish/pending/')
        dishes = [
            model_to_json(PendingFood.objects.get(_id=str(self.dish_2._id)))
        ]
        expected = {'Dishes': dishes}
        self.assertDictEqual(expected, json.loads(response.content))

    def test_edit_dish_valid(self):
        """ Tests if dish is modified correctly """
        edit_dish = {
            "name": "dish 2.1",
            "category": "Specials",
            "specials": "",
            "description": "dish 1 desc",
            "price": "10.50"
        }
        response = self.client.put(
            '/api/dish/pending/'+str(self.dish_2._id)+'/', edit_dish, format='json'
        )
        actual = json.loads(response.content)
        expected = model_to_json(
            PendingFood.objects.get(_id=str(self.dish_2._id))
        )
        self.assertDictEqual(expected, actual)

    def test_delete_dish(self):
        """ Tests if dish is deleted correctly """
        response = self.client.delete('/api/dish/pending/'+str(self.dish_2._id)+'/')
        self.assertFalse(PendingFood.objects.filter(
            _id=str(self.dish_2._id)
        ).exists())


class UserFavRestTestCases(TestCase):
    """ Tests for user-restaurant-favourite relations """

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.bu = User.objects.create(username="TestUser", role="BU", email="bu@mail.com")
        self.ro = User.objects.create(username="TestOwner", role="RO", email="ro@mail.com")
        self.ro_2 = User.objects.create(username="TestOwner2", role="RO", email="ro2@mail.com")
        self.client.force_authenticate(user=self.bu)
        self.restaurant = Restaurant.objects.create(
            name="test",
            owner_user_id=self.ro.id,
            address="431 Kwapis BLVD",
            postalCode="L3X 3H5",
            email="test@mail.com"
        )
        self.restaurant_2 = Restaurant.objects.create(
            name="test 2",
            owner_user_id=self.ro_2.id,
            address="431 Kwapis BLVD",
            postalCode="L3X 3H5",
            email="test2@mail.com"
        )
        self.fav_relation = UserFavRestrs.objects.create(
            user_id=self.bu.id,
            restaurant=str(self.restaurant_2._id)
        )

    def test_insert_fav(self):
        """ Tests if new restaurant is inserted to user's favourites correctly """
        fav_restaurant = {
            "restaurant": str(self.restaurant._id)
        }
        response = self.client.post('/api/user/favourite/', fav_restaurant, format='json')
        self.assertTrue(UserFavRestrs.objects.filter(
            user_id=self.bu.id,
            restaurant=str(self.restaurant._id)
        ).exists())

    def test_get_favs(self):
        """ Tests if all favourited restaurants are retrieved correctly """
        response = self.client.get('/api/user/favourite/')
        actual = json.loads(response.content)
        fav_rest = Restaurant.objects.get(_id=str(self.restaurant_2._id))
        fav_rest.offer_options = ast.literal_eval(fav_rest.offer_options)
        expected = [
            model_to_json(fav_rest)
        ]
        self.assertListEqual(expected, actual)

    def test_delete_fav(self):
        """ Tests if restaurant is removed from user's favourites correctly """
        response = self.client.delete('/api/user/favourite/'+str(self.restaurant_2._id)+'/')
        self.assertFalse(UserFavRestrs.objects.filter(
            user_id=self.bu.id,
            restaurant=str(self.restaurant_2._id)
        ).exists())


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
        self.assertDictEqual(expected, json.loads(response.content))

    def test_get_approved_restaurant(self):
        """ Test if approved restaurant is retrieved by _id """
        _id = Restaurant.objects.get(email="1@mail.com")._id
        response = self.client.get('/api/restaurant/approved/'+str(_id)+'/')

        restaurant = Restaurant.objects.get(email="1@mail.com")
        restaurant.restaurant_image_url = ['/']
        restaurant.payment_methods = ['/']
        restaurant.offer_options = ['']

        expected = model_to_json(restaurant)
        self.assertDictEqual(expected, json.loads(response.content))


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
        self.assertTrue(expected, json.loads(response.content))

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
            status=Status.Pending.name).exists())

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
        self.assertTrue(expected, json.loads(response.content))

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
            status=Status.Pending.name).exists())


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
        self.assertDictEqual(expected, json.loads(response.content))


class RestaurantPostTestCases(TestCase):
    """ Tests for restaurant post creation and retrieval """

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
            model_to_json(RestaurantPost.objects.get(_id=str(self.post_1._id))),
            model_to_json(RestaurantPost.objects.get(_id=str(self.post_2._id)))
        ]

        expected = {"Posts": posts}
        self.assertDictEqual(expected, actual)


class RestaurantPostDeleteTestCases(TestCase):
    """ Tests for restaurant post removal """

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

    def test_delete_post(self):
        """ Test if restaurant post is deleted correctly """
        response = self.client.delete('/api/restaurant/post/'+str(self.post_1._id)+'/')
        self.assertFalse(RestaurantPost.objects.filter(
            _id=str(self.post_1._id)
        ).exists())
        self.assertTrue(RestaurantPost.objects.filter(
            _id=str(self.post_2._id)
        ).exists())


class RestaurantPostPublicTestCases(TestCase):
    """ Tests for restaurant public posts retrieval """

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

    def test_get_post_public(self):
        """ Test if restaurant posts for public view are retrieved correctly """
        response = self.client.get('/api/restaurant/public/post/'+str(self.restaurant._id)+'/')
        actual = json.loads(response.content)
        for post in actual['Posts']:
            post.pop('Timestamp')
        posts = [
            model_to_json(RestaurantPost.objects.get(_id=str(self.post_1._id))),
            model_to_json(RestaurantPost.objects.get(_id=str(self.post_2._id)))
        ]

        expected = {"Posts": posts}
        self.assertDictEqual(expected, actual)
