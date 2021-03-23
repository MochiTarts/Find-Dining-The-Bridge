
from djongo import models
from django.utils import timezone
from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from utils.validators import check_script_injections, validate_url, validate_name, validate_postal_code
from utils.model_util import save_and_clean, update_model_geo, model_refresh, model_to_json
from restaurant.cuisine_dict import load_dict
from restaurant.fields import StringListField, CustomListField
from restaurant.enum import Prices, Categories, Status, Options, Payment

from bson import ObjectId
import requests
import ast
import re

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'
RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'


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
        """
        Retrieve restaurant by id
        :param rest_id: id of restaurant
        :return: restaurant data in json
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
    def add_dish(cls, food_data):
        """
        insert dish into database and return response
        :param food_data: dictionary representation of dish
        :return: Food model object
        """
        try:
            dish = cls(
                name=food_data['name'],
                restaurant_id=food_data['restaurant_id'],
                description=food_data['description'],
                price=food_data['price'],
                specials=food_data['specials'],
                category=food_data['category'],
            )
            save_and_clean(dish)
            restaurant = PendingRestaurant.objects.get(
                _id=food_data['restaurant_id'])
            if not restaurant.category_exists(food_data['category']):
                restaurant.categories.append(food_data['category'])
                restaurant.save(update_fields=['categories'])
            return dish
        except ValidationError as e:
            if 'Ensure this value has at most 50 characters' in str(e):
                raise Exception("Cannot insert dish, the name is too long")
            else:
                raise Exception(str(e))
        except ValueError as e:
            if 'FAILED SQL: INSERT INTO' in str(e):
                raise ValueError(
                    "Cannot insert dish, this already exists for this restaurant")
            else:
                raise Exception(str(e))

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        Retrieve restaurant by id
        :param rest_id: id of restaurant
        :return: restaurant data in json
        """
        return list(PendingFood.objects.filter(restaurant_id=rest_id))

    @classmethod
    def get_all_categories(cls, rest_id):
        """
        Retrieve all categories a restaurant's menu has
        :param: rest_id: id of restaurant
        :return: list of categories a restaurant's menu has
        """
        return list(set(PendingFood.objects.filter(restaurant_id=rest_id).values_list('category', flat=True)))

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
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

    attr_list = ['name', 'phone', 'web_url', 'years',
                 'address', 'streetAddress2', 'streetAddress3',
                 'postalCode', 'owner_first_name', 'owner_last_name',
                 'owner_preferred_name', 'owner_story',
                 'email', 'locationNotes', 'facebook', 'twitter',
                 'instagram', 'bio', 'dineinPickupDetails', 'restaurant_video_url',
                 'restaurant_image_url', ]

    _id = models.ObjectIdField()
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
        """
        Check whether category is new
        @param category: referenced category
        @return: boolean
        """
        return category in self.categories

    @classmethod
    def get(cls, _id):
        """
        retrieve restaurant based on id
        :param _id: id of restaurant
        :return: restaurant json or None
        """
        try:
            restaurant = Restaurant.objects.get(_id=_id)
            return restaurant
        except ObjectDoesNotExist:
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
        """
        retrieve restaurant based on id
        :param _id: id of restaurant
        :return: restaurant json or None
        """
        try:
            restaurant = PendingRestaurant.objects.get(_id=_id)
            return restaurant
        except ObjectDoesNotExist:
            return None

    @classmethod
    def insert(cls, restaurant_data):
        """
        Insert pending restaurant into database given restaurant data
        :param restaurant_data: json data of restaurant
        :return: restaurant object representing sent data
        """
        try:
            cls.objects.get(email=restaurant_data['email'])
            raise ValueError(
                'Cannot insert pending restaurant object, an object with this email already exists')
        except ObjectDoesNotExist:
            restaurant = cls(
                **restaurant_data
            )
            address = restaurant_data['address'] + ', ' + \
                restaurant_data['postalCode'] + ', Ontario'
            update_model_geo(restaurant, address)
            restaurant = save_and_clean(restaurant)
            return restaurant

    @classmethod
    def field_validate_draft(self, fields):
        """
        Validates only the required fields for inserting a restaurant draft
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
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
        """
        Validates all fields of a restaurant for admin approval
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
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
    def insert(cls, data):
        """ Inserts a new user-restaurant favourite relation
        :param: data: dictionary containing user_id and restaurant_id of user and restaurant
                      to be added in a favourite relation
        :return: user-restaurant-favourite relation object with actual restaurant data of
                 the favourite restaurant,
                 or raises ValueError if relation already exists; user or restaurant
                 does not exist
        """
        try:
            consumer_filter = ConsumerSubscriber.objects.filter(user_id=data['user_id'])
            restaurant_owner_filter = RestaurantOwner.objects.filter(user_id=data['user_id'])
            user = {}
            if consumer_filter.exists():
                user = consumer_filter.first()
            elif restaurant_owner_filter.exists():
                user = restaurant_owner_filter.first()
            else:
                raise ValueError('The user does not exist')
            restaurant = Restaurant.objects.get(_id=data['restaurant'])

            try:
                cls.objects.get(user_id=data['user_id'], restaurant=data['restaurant_id'])
                raise ValueError('Cannot insert new user-restaurant-favourite relation, this relation already exists')
            except ObjectDoesNotExist:
                userFavRestr = cls(**data)
                userFavRestr = save_and_clean(userFavRestr)
                response = model_to_json(userFavRestr)

                response['user'] = model_to_json(user)
                response['restaurant'] = model_to_json(restaurant)
                return response
        except ObjectDoesNotExist:
            raise ValueError('The restaurant does not exist')

    @classmethod
    def getUserFavourites(cls, user_id):
        """
        retrieve all restaurants favourited by user given user's email
        :param: user_email: email of user to retrieve list of favourited restaurants
        :return: list of restaurants in json format
        """
        restaurants = []

        consumer_filter = ConsumerSubscriber.objects.filter(user_id=user_id)
        restaurant_owner_filter = RestaurantOwner.objects.filter(user_id=user_id)
        user = {}
        if consumer_filter.exists():
            user = consumer_filter.first()
        elif restaurant_owner_filter.exists():
            user = restaurant_owner_filter.first()
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
                raise ValueError('One of the restaurants in the list of favourites does not appear to exist: '+restaurant._id)
        return restaurants

    @classmethod
    def getRestrFavouriteds(cls, restaurant_id):
        """
        retrieve all users who have favourited this restaurant given the
        restaurant_id
        :param: restaurant_id: id of the restaurant whose list of favourited users to retrieve
        :return: list of users who favourited this restaurant
        """
        users = []

        try:
            Restaurant.objects.get(_id=restaurant_id)
        except ObjectDoesNotExist:
            raise ValueError('The restaurant associated with id '+restaurant_id+' does not exist')

        favouriteds = UserFavRestrs.objects.filter(restaurant_id=restaurant_id)
        if not favouriteds:
            return users
        for record in favouriteds:
            consumer_filter = ConsumerSubscriber.objects.filter(user_id=record.user_id)
            restaurant_owner_filter = RestaurantOwner.objects.filter(user_id=record.user_id)
            if consumer_filter.exists():
                user = consumer_filter.first()
                users.append(model_to_json(user))
            elif restaurant_owner_filter.exists():
                user = restaurant_owner_filter.first()
                users.append(model_to_json(user))
            else:
                raise ValueError('One of the users in the list of favourites does not appear to exist: '+record.user)
        return users

    @classmethod
    def remove_fav(self, data):
        """
        removes a restaurant from the user's favourites list
        :param: data: the id of the restaurant to be removed from the user's list,
                      and the email of the user whose list is going to be updated
        :return: Message with success or raise ValueError upon exceptions
        """
        try:
            consumer_filter = ConsumerSubscriber.objects.filter(user_id=data['user_id'])
            restaurant_owner_filter = RestaurantOwner.objects.filter(user_id=data['user_id'])
            user = {}
            if consumer_filter.exists():
                user = consumer_filter.first()
            elif restaurant_owner_filter.exists():
                user = restaurant_owner_filter.first()
            else:
                raise ValueError('The user does not exist')
        except ObjectDoesNotExist:
            raise ValueError('The user or restaurant does not exist')

        try:
            UserFavRestrs.objects.get(user_id=data['user_id'], restaurant_id=data['restaurant_id']).delete()
            response = {
                "message": "Successfully removed restaurant from user's favourites"
            }
            return response
        except ObjectDoesNotExist:
            raise ValueError('This user-restaurant favourite relation does not exist')

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields (user_id and restaurant_id)
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """

        invalid = {'Invalid': []}

        if 'user_id' in fields:
            try:
                if not fields['user'].isnumeric():
                    invalid['Invalid'].append('user_id')
            except ValidationError as e:
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
