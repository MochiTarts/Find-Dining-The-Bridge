
from djongo import models
from django.utils import timezone
from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model

from utils.validators import check_script_injections, validate_url, validate_name, validate_postal_code
from utils.model_util import save_and_clean, update_model_geo, model_refresh, model_to_json
from restaurant.cuisine_dict import load_dict
from restaurant.fields import StringListField, CustomListField
from restaurant.enum import Prices, Categories, Status, Options, Payment
from sduser.models import SDUser

from bson import ObjectId
import requests
import ast
import re

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'
RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'

User = get_user_model()


class Food(models.Model):
    """ Model for the Food Items on the Menu """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True,
                               default=FOOD_PICTURE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    specials = models.CharField(max_length=51, blank=True)
    category = models.CharField(max_length=50, blank=True, default='')
    status = models.CharField(
        max_length=200, default=Status.Approved.value, choices=Status.choices())

    class Meta:
        unique_together = (("name", "restaurant_id", "category",),)
        verbose_name = "Food (Live)"
        verbose_name_plural = "Foods (Live)"

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """ Retrieve restaurant by id

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :return: restaurant data in json
        :rtype: json
        """
        return list(Food.objects.filter(restaurant_id=rest_id))

    def clean_description(self):
        description = {food for food in self.description.split(' ')}
        clean_description = set()
        for word in description:  # clean word, remove non alphabetical
            clean_description.add(''.join(e for e in word if e.isalpha()))
        clean_description = set(map(str.lower, clean_description))
        return clean_description


class PendingFood(models.Model):
    """ Model for the Food Items on the Menu """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True,
                               default=FOOD_PICTURE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    specials = models.CharField(max_length=51, blank=True)
    category = models.CharField(max_length=50, blank=True, default='')
    status = models.CharField(
        max_length=200, default=Status.Pending.value, choices=Status.choices())

    # for display (default was "objectname object (object_id)")

    def __str__(self):
        return self.name

    class Meta:
        # avoid confusion on 'pending' as it stores both pending/aproved ones
        unique_together = (("name", "restaurant_id", "category",),)
        verbose_name = "Food (Submission)"
        verbose_name_plural = "Foods (Submission)"
        ordering = ['-status']

    @classmethod
    def add_dish(cls, food_data, rest_id):
        """ Insert dish into database and return response

        :param: food_data: dictionary representation of dish
        :type food_data: json
        :param: rest_id: id of the restaurant the dish is associated with
        :type rest_id: ObjectId string
        :return: PendingFood object of the newly inserted record
        :rtype: PendingFood object
        """
        if not PendingRestaurant.objects.filter(_id=rest_id).exists():
            raise ValueError("The restaurant does not exist")

        if cls.objects.filter(name=food_data['name'], restaurant_id=rest_id, category=food_data['category']).exists():
            raise ValueError(
                "Cannot insert dish, this already exists for this restaurant")
        else:
            dish = cls(
                name=food_data['name'],
                restaurant_id=rest_id,
                description=food_data['description'],
                price=food_data['price'],
                specials=food_data['specials'],
                category=food_data['category'],
            )
            save_and_clean(dish)
            restaurant = PendingRestaurant.objects.get(_id=rest_id)
            if not restaurant.category_exists(food_data['category']):
                restaurant.categories.append(food_data['category'])
                restaurant.save(update_fields=['categories'])
            return dish

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """ Retrieve restaurant by id

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :return: restaurant data in json
        :rtype: list
        """
        return list(PendingFood.objects.filter(restaurant_id=rest_id))

    @classmethod
    def get_all_categories(cls, rest_id):
        """ Retrieve all categories a restaurant's menu has

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :return: list of categories a restaurant's menu has
        :rtype: list
        """
        return list(set(PendingFood.objects.filter(restaurant_id=rest_id).values_list('category', flat=True)))

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :type: json object
        """
        dish_urls = ['picture']
        invalid = {'Invalid': []}

        for field in dish_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        if not invalid['Invalid']:
            return None
        else:
            return invalid

    def clean_description(self):
        description = {food for food in self.description.split(' ')}
        clean_description = set()
        for word in description:  # clean word, remove non alphabetical
            clean_description.add(''.join(e for e in word if e.isalpha()))
        clean_description = set(map(str.lower, clean_description))
        return clean_description


class Restaurant(models.Model):
    """ Model for Restaurants """
    _id = models.ObjectIdField()
    owner_user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    years = models.IntegerField(null=True)
    address = models.CharField(max_length=60)
    streetAddress2 = models.CharField(max_length=50, blank=True, default='')
    streetAddress3 = models.CharField(max_length=50, blank=True, default='')
    postalCode = models.CharField(max_length=7, default='')

    phone = models.BigIntegerField(null=True)
    email = models.EmailField(unique=True)
    pricepoint = models.CharField(max_length=10, choices=Prices.choices())
    cuisines = CustomListField(default=[], blank=True)

    offer_options = models.TextField(default='[""]')

    dineinPickupDetails = models.TextField(
        null=True, blank=True, default='', max_length=2000)
    deliveryDetails = models.TextField(
        null=True, blank=True, default='', max_length=2000)
    locationNotes = models.CharField(max_length=2000,  blank=True, default='')

    web_url = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(max_length=200)
    cover_photo_url = models.CharField(max_length=200,
                                       default='https://storage.googleapis.com/default-assets/cover.jpg')
    logo_url = models.CharField(max_length=200,
                                default='https://storage.googleapis.com/default-assets/logo.jpg')
    restaurant_video_url = models.CharField(max_length=200, default='/')
    restaurant_image_url = models.TextField(default='["/"]', blank=True)

    owner_first_name = CustomListField(default=[], blank=True)
    owner_last_name = CustomListField(default=[], blank=True)
    owner_preferred_name = CustomListField(default=[], blank=True)
    owner_story = models.CharField(max_length=2000, blank=True)
    owner_picture_url = models.CharField(max_length=200, blank=True)

    categories = CustomListField(default=[], blank=True)
    status = models.CharField(
        max_length=200, default=Status.Approved.value, choices=Status.choices())

    sysAdminComments = models.CharField(
        blank=True, default='', max_length=2000)

    open_hours = models.TextField(default='')
    payment_methods = models.TextField(default='["/"]')

    full_menu_url = models.CharField(max_length=200, blank=True)
    approved_once = models.BooleanField(default=False, blank=True)

    # for display (default was "objectname object (object_id)")
    def __str__(self):
        return self.name

    class Meta:
        # Add 'Live' to distinguish it from the submission one
        verbose_name = "Restaurant (Live)"
        verbose_name_plural = "Restaurants (Live)"
        # ordering = ['-status', 'modified_time']

    def category_exists(self, category):
        """ Check whether category is new

        :param category: referenced category
        :type category: string
        :return: A boolean representing if a category exists in the restaurant's categories field
        :type: boolean
        """
        return category in self.categories

    @classmethod
    def get(cls, _id):
        """ retrieve restaurant based on id

        :param _id: id of restaurant
        :type _id: ObjectId string
        :return: restaurant json or None
        :rtype: json object or None
        """
        restaurant_filter = cls.objects.filter(_id=_id)
        if restaurant_filter.exists() and restaurant_filter.count() == 1:
            restaurant = restaurant_filter.first()
            return restaurant
        else:
            return None


class PendingRestaurant(models.Model):
    """ Model for Restaurants """

    attr_list = [
        'name', 'phone', 'web_url', 'years',
        'address', 'streetAddress2', 'streetAddress3',
        'postalCode', 'owner_first_name', 'owner_last_name',
        'owner_preferred_name', 'owner_story',
        'email', 'locationNotes', 'facebook', 'twitter',
        'instagram', 'bio', 'dineinPickupDetails', 'restaurant_video_url',
        'restaurant_image_url', 'full_menu_url',
    ]

    _id = models.ObjectIdField()
    name = models.CharField(max_length=30, blank=True, default='')
    owner_user_id = models.IntegerField(blank=True, null=True)
    years = models.IntegerField(null=True, blank=True, default=0)
    address = models.CharField(max_length=60, blank=True, default='')
    streetAddress2 = models.CharField(max_length=50, blank=True, default='')
    streetAddress3 = models.CharField(max_length=50, blank=True, default='')
    postalCode = models.CharField(max_length=7, default='', blank=True)

    phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    pricepoint = models.CharField(
        max_length=10, choices=Prices.choices(), blank=True)
    cuisines = CustomListField(default=[], blank=True)

    offer_options = models.TextField(default='[""]', blank=True)

    dineinPickupDetails = models.TextField(
        null=True, blank=True, default='', max_length=2000)
    deliveryDetails = models.TextField(
        null=True, blank=True, default='', max_length=2000)
    locationNotes = models.CharField(max_length=2000,  blank=True, default='')

    web_url = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True, blank=True)
    GEO_location = models.CharField(max_length=200, blank=True)
    cover_photo_url = models.CharField(max_length=200,
                                       default='https://storage.googleapis.com/default-assets/cover.jpg', blank=True)
    logo_url = models.CharField(max_length=200,
                                default='https://storage.googleapis.com/default-assets/logo.jpg', blank=True)
    restaurant_video_url = models.CharField(
        max_length=200, default='/', blank=True)
    restaurant_image_url = models.TextField(default='["/"]', blank=True)

    owner_first_name = CustomListField(default=[], blank=True)
    owner_last_name = CustomListField(default=[], blank=True)
    owner_preferred_name = CustomListField(default=[], blank=True)
    owner_story = models.CharField(max_length=3000, blank=True)
    owner_picture_url = models.CharField(max_length=200, blank=True)

    categories = CustomListField(default=[], blank=True)
    status = models.CharField(
        max_length=200, default=Status.In_Progress.value, choices=Status.choices())

    sysAdminComments = models.CharField(
        blank=True, default='', max_length=2000)

    modified_time = models.DateTimeField(
        editable=False, null=True, default=timezone.now)

    open_hours = models.TextField(default='', blank=True)
    payment_methods = models.TextField(default='["/"]', blank=True)

    full_menu_url = models.CharField(max_length=200, blank=True)
    approved_once = models.BooleanField(default=False, blank=True)

    # for display (default was "objectname object (object_id)")
    def __str__(self):
        return self.name

    class Meta:
        # avoid confusion on 'pending' as it stores both pending/aproved ones
        # Add 'Submission' to distinguish it from the live one
        verbose_name = "Restaurant (Submission)"
        verbose_name_plural = "Restaurants (Submission)"
        ordering = ['-status', 'modified_time']

    @classmethod
    def get(cls, _id):
        """ retrieve restaurant based on id

        :param _id: id of restaurant
        :type _id: ObjectId string
        :return: restaurant json or None
        :rtype: json object or None
        """
        restasurant_filter = cls.objects.filter(_id=_id)
        if restasurant_filter.exists() and restasurant_filter.count() == 1:
            restaurant = restasurant_filter.first()
            return restaurant
        else:
            return None

    @classmethod
    def insert(cls, restaurant_data):
        """ Insert pending restaurant into database given restaurant data

        :param restaurant_data: json data of restaurant
        :type restaurant_data: json
        :raises ValueError: if the pending restaurant already exists in the database
        :return: restaurant object representing sent data
        :rtype: :class:`PendingRestaurant` object
        """
        if cls.objects.filter(email=restaurant_data['email']).exists():
            raise ValueError(
                'Cannot insert pending restaurant object, an object with this email already exists')
        else:
            restaurant = cls(
                **restaurant_data
            )
            address = restaurant_data['address'] + ', ' + \
                restaurant_data['postalCode'] + ', Ontario'
            update_model_geo(restaurant, address)
            restaurant = save_and_clean(restaurant)
            return restaurant

    def category_exists(self, category):
        """ Check whether category is new

        :param category: referenced category
        :type category: string
        :return: A boolean representing if a category exists in the restaurant's categories field
        :type: boolean
        """
        return category in self.categories

    @classmethod
    def field_validate_draft(self, fields):
        """ Validates only the required fields for inserting a restaurant draft

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :rtype: json object
        """
        invalid = {'Invalid': []}

        if 'name' in fields and not fields['name']:
            invalid['Invalid'].append('name')

        if 'address' in fields and not fields['address']:
            invalid['Invalid'].append('address')

        if 'postalCode' in fields:
            try:
                validate_postal_code(fields['postalCode'])
                if not fields['postalCode']:
                    invalid['Invalid'].append('postalCode')
            except ValidationError:
                invalid['Invalid'].append('postalCode')

        if 'email' in fields:
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')

        if 'owner_first_name' in fields and fields['owner_first_name']:
            try:
                for name in fields['owner_first_name']:
                    if not name:
                        invalid['Invalid'].append('owner_last_name')
                        break
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_first_name')

        if 'owner_last_name' in fields and fields['owner_last_name']:
            try:
                for name in fields['owner_last_name']:
                    if not name:
                        invalid['Invalid'].append('owner_last_name')
                        break
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_last_name')

        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid

    @classmethod
    def field_validate(self, fields):
        """ Validates all fields of a restaurant for admin approval

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :rtype: json object
        """
        invalid = {'Invalid': []}

        # check if there is script in any field values
        for attr in self.attr_list:
            if attr in fields:
                value = fields[attr]
                if value is not None:
                    try:
                        check_script_injections(value)
                    except ValidationError as e:
                        invalid['Invalid'].append(attr)

        if 'name' in fields and not fields['name']:
            invalid['Invalid'].append('name')

        if 'years' in fields:
            if fields['years'] is not None:
                if not str(fields['years']).isnumeric():
                    invalid['Invalid'].append('years')
            else:
                invalid['Invalid'].append('years')

        if 'address' in fields and not fields['address']:
            invalid['Invalid'].append('address')

        if 'postalCode' in fields:
            try:
                validate_postal_code(fields['postalCode'])
                if not fields['postalCode']:
                    invalid['Invalid'].append('postalCode')
            except ValidationError:
                invalid['Invalid'].append('postalCode')

        if 'phone' in fields:
            if fields['phone'] is not None:
                if len(str(fields['phone'])) != 10 and str(fields['phone']).isnumeric():
                    invalid['Invalid'].append('phone')
            else:
                invalid['Invalid'].append('phone')

        if 'email' in fields:
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')

        if 'pricepoint' in fields:
            if fields['pricepoint'] is not None:
                if not Prices.has_key(fields['pricepoint']):
                    invalid['Invalid'].append('pricepoint')
            else:
                invalid['Invalid'].append('pricepoint')

        if 'web_url' in fields and fields['web_url'] != "":
            website = fields['web_url']
            try:
                validate_url(website)
            except ValidationError as e:
                invalid['Invalid'].append('website')

        if 'facebook' in fields and fields['facebook'] != "":
            website = fields['facebook']
            try:
                validate_url(website)
            except ValidationError as e:
                invalid['Invalid'].append('facebook')

        if 'twitter' in fields and fields['twitter'] != "":
            website = fields['twitter']
            try:
                validate_url(website)
            except ValidationError as e:
                invalid['Invalid'].append('twitter')

        if 'instagram' in fields and fields['instagram'] != "":
            website = fields['instagram']
            try:
                validate_url(website)
            except ValidationError as e:
                invalid['Invalid'].append('instagram')

        if 'owner_first_name' in fields and fields['owner_first_name']:
            try:
                for name in fields['owner_first_name']:
                    if not name:
                        invalid['Invalid'].append('owner_last_name')
                        break
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_first_name')

        if 'owner_last_name' in fields and fields['owner_last_name']:
            try:
                for name in fields['owner_last_name']:
                    if not name:
                        invalid['Invalid'].append('owner_last_name')
                        break
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_last_name')

        if 'open_hours' in fields and not fields['open_hours']:
            invalid['Invalid'].append('open_hours')

        if 'payment_methods' in fields:
            if fields['payment_methods']:
                for payment in fields['payment_methods']:
                    if payment not in Payment.values():
                        invalid['Invalid'].append('payment_methods')
            else:
                invalid['Invalid'].append('payment_methods')

        if 'full_menu_url' in fields and fields['full_menu_url'] != "":
            website = fields['full_menu_url']
            try:
                validate_url(website)
            except ValidationError as e:
                invalid['Invalid'].append('full_menu_url')

        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid


class UserFavRestrs(models.Model):
    """ Model for displaying user-restaurant-favourite relation """
    _id = models.ObjectIdField()
    user_id = models.IntegerField(default=None)
    restaurant = models.CharField(default='', max_length=24)

    @classmethod
    def insert(cls, user_id, rest_id):
        """ Inserts a new user-restaurant favourite relation

        :param user_id: the id of the user for this user-restaurant favourite relation
        :type user_id: int
        :param rest_id: the id of the restaurant for this user-restaurant favourite relation
        :type rest_id: ObjectId string
        :raises ValueError: if the relation already exists, or the user or restaurant does not exist
        :return: user-restaurant-favourite relation object with actual restaurant data of
                 the favourite restaurant
        :rtype: json object
        """
        user_filter = User.objects.filter(id=user_id)
        restaurant_filter = Restaurant.objects.filter(_id=rest_id)
        user = {}
        restaurant = {}
        if not user_filter.exists():
            raise ValueError('The user does not exist')
        elif user_filter.count() > 1:
            raise ValueError('There are more than one user with this user_id')
        else:
            user = user_filter.first()

        if not restaurant_filter.filter(_id=rest_id).exists():
            raise ValueError('The restaurant does not exist')
        elif restaurant_filter.count() > 1:
            raise ValueError('There are more than one restaurant with this restaurant_id')
        else:
            restaurant = restaurant_filter.first()

        if cls.objects.filter(user_id=user_id, restaurant=rest_id).exists():
            raise ValueError('Cannot insert new user-restaurant-favourite relation, this relation already exists')
        userFaveRest = cls(user_id=user_id, restaurant=rest_id)
        userFaveRest = save_and_clean(userFaveRest)
        response = model_to_json(userFaveRest)
        response['user_id'] = model_to_json(user)
        response['restaurant'] = model_to_json(restaurant)
        return response

    @classmethod
    def getUserFavourites(cls, user_id):
        """ retrieve all restaurants favourited by user given user's id

        :param user_id: id of user to retrieve list of favourited restaurants
        :type user_id: int
        :raises ValueError: if one of the restaurants in the list of user's favourites does not exist
        :return: list of restaurants in json format
        :rtype: list of json objects
        """
        restaurants = []

        user_filter = User.objects.filter(id=user_id)
        user = {}
        if user_filter.exists() and user_filter.count() == 1:
            user = user_filter.first()
        else:
            raise ValueError('The user does not exist')

        favourites = UserFavRestrs.objects.filter(user_id=user_id)
        if not favourites:
            return restaurants
        for record in favourites:
            try:
                restaurant = Restaurant.objects.get(_id=record.restaurant)
                restaurant.offer_options = ast.literal_eval(restaurant.offer_options)
                restaurants.append(model_to_json(restaurant))
            except ObjectDoesNotExist:
                raise ValueError(
                    'One of the restaurants in the list of favourites does not appear to exist: '+record.restaurant)
        return restaurants

    @classmethod
    def getRestrFavouriteds(cls, restaurant_id):
        """ retrieve all users who have favourited this restaurant given the restaurant_id

        :param restaurant_id: id of the restaurant whose list of favourited users to retrieve
        :type restaurant_id: ObjectId string
        :raises ValueError: if the restaurant does not exist, 
                            or one of the users who favourited this restaurant does not exist
        :return: list of users who favourited this restaurant
        :rtype: list of json objects
        """
        users = []

        if not Restaurant.objects.filter(_id=restaurant_id).exists():
            raise ValueError('The restaurant associated with id '+restaurant_id+' does not exist')

        favouriteds = UserFavRestrs.objects.filter(restaurant=restaurant_id)
        if not favouriteds:
            return users
        for record in favouriteds:
            user_filter = User.objects.filter(id=record.user_id)
            if user_filter.exists():
                user = user_filter.first()
                users.append(model_to_json(user))
            else:
                raise ValueError('One of the users in the list of favourites does not appear to exist: '+record.user)
        return users

    @classmethod
    def remove_fav(cls, user_id, rest_id):
        """ removes a restaurant from the user's favourites list

        :param user_id: the id of the user whose list of favourites will have one restaurant removed
        :type user_id: int
        :param rest_id: the id of the restaurant to be removed from the user's list
        :type rest_id: ObjectId string
        :raises ValueError: if the user does not exist or the user-restaurant favourite relation does not exist
        :return: Message with success or raise ValueError upon exceptions
        :rtype: json object
        """
        user_filter = User.objects.filter(id=user_id)
        user = {}
        if user_filter.exists():
            user = user_filter.first()
        else:
            raise ValueError('The user does not exist')

        user_fav_filter = UserFavRestrs.objects.filter(user_id=user_id, restaurant=rest_id)
        if user_fav_filter.exists():
            user_fav_filter.delete()
            response = {
                "message": "Successfully removed restaurant from user's favourites"
            }
            return response
        else:
            raise ValueError('This user-restaurant favourite relation does not exist')

    @classmethod
    def field_validate(self, fields):
        """ Validates fields (user_id and restaurant_id)

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :rtype: list
        """

        invalid = {'Invalid': []}

        if 'user_id' in fields:
            if fields['user_id']:
                if not str(fields['user_id']).isnumeric():
                    invalid['Invalid'].append('user_id')
            else:
                invalid['Invalid'].append('user_id')

        if 'restaurant_id' in fields:
            try:
                ObjectId(fields['restaurant_id'])
            except Exception:
                invalid['Invalid'].append('restaurant_id')

        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid


class RestaurantPost(models.Model):
    """ Model for a restaurant post """
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    owner_user_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(max_length=4096)
    timestamp = models.DateTimeField(auto_now=True)

    @classmethod
    def insert(cls, post_data:dict):
        """ Inserts a new post into the database

        :param post_data: data of the post to be inserted
        :type post_data: dict
        :return: the newly inserted post record
        :rtype: :class: `RestaurantPost`
        """
        post = RestaurantPost(**post_data)
        post = save_and_clean(post)
        return post

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :return: A list of fields that were invalid. Returns None if all fields are valid
        :rtype: list
        """

        invalid = {'Invalid': []}

        if 'restaurant_id' in fields:
            try:
                ObjectId(fields['restaurant_id'])
            except Exception:
                invalid['Invalid'].append('restaurant_id')

        if 'content' in fields:
            if not fields['content']:
                invalid['Invalid'].append('content')


        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid