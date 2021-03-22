
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
    def add_dish(cls, food_data):
        """
        insert dish into database and return response
        :param food_data: dictionary representation of dish
        :return: Food model object
        """
        dish = cls(
            name=food_data['name'],
            restaurant_id=food_data['restaurant_id'],
            description=food_data['description'],
            price=food_data['price'],
            specials=food_data['specials'],
            category=food_data['category'],
        )
        save_and_clean(dish)
        dish = model_refresh(
            Food, {'name': dish.name, 'restaurant_id': dish.restaurant_id})
        restaurant = Restaurant.objects.get(_id=food_data['restaurant_id'])
        if not restaurant.category_exists(food_data['category']):
            restaurant.categories.append(food_data['category'])
            restaurant.save(update_fields=['categories'])
        return dish

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        Retrieve restaurant by id
        :param rest_id: id of restaurant
        :return: restaurant data in json
        """
        return list(Food.objects.filter(restaurant_id=rest_id))

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

    @classmethod
    def insert(cls, restaurant_data):
        """
        Insert restaurant into database given restaurant data
        :param restaurant_data: json data of restaurant
        :return: restaurant object representing sent data
        """
        try:
            cls.objects.get(email=restaurant_data['email'])
            raise ValueError(
                'Cannot insert restaurant object, an object with this email already exists')
        except ObjectDoesNotExist:
            restaurant = cls(
                **restaurant_data
            )
            update_model_geo(restaurant, restaurant_data['address'])
            restaurant = save_and_clean(restaurant)
            return restaurant

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """
        restaurant_urls = ['twitter', 'instagram', 'cover_photo_url', 'logo_url', 'owner_picture_url',
                           'external_delivery_link']

        invalid = {'Invalid': []}

        for field in restaurant_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        # check if there is script in any field values
        for attr in self.attr_list:
            if attr in fields:
                value = fields[attr]
                if value is not None:
                    try:
                        check_script_injections(value)
                    except ValidationError as e:
                        invalid['Invalid'].append(attr)

        for field in restaurant_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)
        if 'owner_first_name' in fields and fields['owner_first_name']:
            try:
                for name in fields['owner_first_name']:
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_first_name')

        if 'owner_last_name' in fields and fields['owner_last_name']:
            try:
                for name in fields['owner_last_name']:
                    validate_name(name)
            except ValidationError as e:
                invalid['Invalid'].append('owner_last_name')
        else:
            invalid['Invalid'].append('owner_last_name')

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

        if 'email' in fields:
            # if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", fields['email']):
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')
        else:
            invalid['Invalid'].append('email')

        if 'phone' in fields and fields['phone'] is not None:
            if len(str(fields['phone'])) != 10 and str(fields['phone']).isnumeric():
                invalid['Invalid'].append('phone')

        if not 'open_hours' in fields:
            invalid['Invalid'].append('open hours')

        if 'payment_methods' in fields and fields['payment_methods']:
            for payment in fields['payment_methods']:
                if payment not in Payment.values():
                    invalid['Invalid'].append(
                        'payment_methods ('+payment+' is not a valid payment method. Should be credit, debit, or cash)')

        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid


class PendingRestaurant(models.Model):
    """ Model for Restaurants """

    attr_list = ['name', 'phone', 'web_url', 'years',
                 'address', 'streetAddress2', 'streetAddress3',
                 'postalCode', 'owner_first_name', 'owner_last_name',
                 'owner_preferred_name', 'owner_story',
                 'email', 'locationNotes', 'facebook', 'twitter',
                 'instagram', 'bio', 'dineinPickupDetails', 'restaurant_video_url',
                 'restaurant_image_url', 'full_menu_url', ]

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
            restaurant = PendingRestaurant.objects.get(_id=_id)
            return restaurant
        except ObjectDoesNotExist:
            return None

    @classmethod
    def insert(cls, restaurant_data):
        """
        Insert restaurant into database given restaurant data
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

        if 'email' in fields:
            # if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", fields['email']):
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')

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
        restaurant_urls = ['twitter', 'instagram', 'cover_photo_url', 'logo_url', 'owner_picture_url',
                           'external_delivery_link', 'full_menu_url']

        invalid = {'Invalid': []}

        for field in restaurant_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        # check if there is script in any field values
        for attr in self.attr_list:
            if attr in fields:
                value = fields[attr]
                if value is not None:
                    try:
                        check_script_injections(value)
                    except ValidationError as e:
                        invalid['Invalid'].append(attr)

        for field in restaurant_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

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

        if 'email' in fields:
            # if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", fields['email']):
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

        if 'phone' in fields:
            if fields['phone'] is not None:
                if len(str(fields['phone'])) != 10 and str(fields['phone']).isnumeric():
                    invalid['Invalid'].append('phone')
            else:
                invalid['Invalid'].append('phone')

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
