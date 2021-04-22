
from djongo import models
from django.utils import timezone
from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from sduser.models import SDUser
from utils.model_util import save_and_clean, update_model_geo, model_refresh, model_to_json, edit_model
from utils.cloud_storage import upload, delete, IMAGE, VIDEO, DEV_BUCKET
from utils.validators import (
    check_script_injections,
    validate_url,
    validate_name,
    validate_postal_code,
    validate_profane_content
)
from restaurant.cuisine_dict import load_dict
from restaurant.utils import send_posts_notify_email
from restaurant.fields import StringListField, CustomListField
from restaurant.enum import (
    Prices,
    Categories,
    Status,
    Options,
    Payment,
    MediaType,
    RestaurantSaveLocations,
    FoodSaveLocations
)

from rest_framework.exceptions import NotFound

import json
from bson import ObjectId
import requests
import ast
import re

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'
RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'

dish_editable = ["name", "description", "picture",
                 "price", "specials", "category", "status"
                 ]

restaurant_editable = [
    "name",
    "years",
    "address",
    "streetAddress2",
    "streetAddress3",
    "postalCode",
    "phone",
    "updated_at",
    "cuisines",
    "pricepoint",
    "offer_options",
    "deliveryDetails",
    "locationNotes",
    "dineinPickupDetails",
    "web_url",
    "facebook",
    "twitter",
    "instagram",
    "bio",
    "cover_photo_url",
    "logo_url",
    "restaurant_video_url",
    "restaurant_image_url",
    "owner_first_name",
    "owner_last_name",
    "owner_preferred_name",
    "owner_story",
    "owner_picture_url",
    "status",
    "modified_time",
    "sysAdminComments",
    "open_hours",
    "payment_methods",
    "full_menu_url",
    "restaurant_video_desc"]

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
        max_length=200,
        default=Status.Approved.value,
        choices=Status.choices())

    class Meta:
        unique_together = (("name", "restaurant_id", "category",),)
        verbose_name = "Food (Live)"
        verbose_name_plural = "Foods (Live)"

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """ Retrieves Restaurant record by its id,
        given by rest_id param

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :return: restaurant data in json
        :rtype: json
        """
        return list(Food.objects.filter(restaurant_id=rest_id))


class PendingFood(models.Model):
    """ Pending version of the model for the Food Items on the Menu """
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
        :raises: ObjectDoesNotExist when the PendingRestaurant of rest_id does not exist
        :raises: IntegrityError upon any violation of business logic
        :return: PendingFood object of the newly inserted record
        :rtype: PendingFood object
        """
        if not PendingRestaurant.objects.filter(_id=rest_id).exists():
            raise ObjectDoesNotExist("The restaurant does not exist")

        if cls.objects.filter(restaurant_id=rest_id).count() == 12:
            raise IntegrityError(
                "Have exceeded the maximum limit of 12 dishes")

        if cls.objects.filter(
                name=food_data['name'],
                restaurant_id=rest_id,
                category=food_data['category']).exists():
            raise IntegrityError(
                "Cannot insert dish, this already exists for this restaurant")

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
    def edit_dish(cls, dish_id, food_data, rest_id):
        """ Updates a dish given its _id, updated fields and its
        associated restaurant id

        :param dish_id: the id of the dish
        :type dish_id: ObjectId str
        :param food_data: the dish fields containing the updated values
        :type food_data: dict
        :param rest_id: the id of the restaurant the dish belongs to
        :type rest_id: ObjectId str
        :raises: ObjectDoesNotExist when the PendingFood to be edited does not exist
        :return: updated PendingFood object
        :rtype: :class: `PendingFood`
        """
        dish = cls.objects.filter(_id=dish_id).first()
        if not dish:
            raise ObjectDoesNotExist(
                "The dish with this _id: " + dish_id + " does not exist")
        restaurant = PendingRestaurant.objects.filter(_id=rest_id).first()
        if not restaurant:
            raise ObjectDoesNotExist(
                "The restaurant with _id: " + rest_id + " does not exist")
        if cls.should_add_category(food_data, dish.category, restaurant):
            cls.add_category(dish.category, restaurant)

        check_dish = cls.objects.filter(
            name=food_data['name'], category=food_data['category'], restaurant_id=rest_id)
        if check_dish.exists() and dish_id != str(check_dish.first()._id):
            raise IntegrityError(
                "You already have a dish named "+food_data['name']+" in the "+food_data['category']+" category")

        restaurant_editable = ["status"]
        restaurant_editable_values = {'status': Status.In_Progress.value}

        if 'category' in food_data and cls.objects.filter(
                restaurant_id=rest_id, category=food_data['category']).exists():
            restaurant_editable.append("categories")

        food_data["status"] = Status.Pending.value
        dish_editable = [field for field in food_data.keys()]
        edit_model(dish, food_data, dish_editable)
        dish = save_and_clean(dish, dish_editable)

        if 'categories' in restaurant_editable:
            restaurant_editable_values['categories'] = cls.get_all_categories(
                restaurant._id)
        edit_model(restaurant, restaurant_editable_values, restaurant_editable)
        save_and_clean(restaurant)
        return dish

    @classmethod
    def remove_dish(cls, dish_id, rest_id):
        """ Deletes a dish and its approved version (if it exists) from
        the database, given data about it. Updates the categories of its associated
        restaurant given the rest_id if necessary

        :param rest_id: the id of the associated restaurant
        :type rest_id: ObjectId str
        :raises ObjectDoesNotExist: when the PendingFood does not exist
        :return: the deleted dish record
        :rtype: :class: `PendingFood`
        """
        food = cls.objects.filter(_id=dish_id)
        if not food.first():
            raise ObjectDoesNotExist("The food to be deleted does not exist")
        deleted_food = food.first()
        food.delete()

        Food.objects.filter(_id=dish_id).delete()

        restaurant = PendingRestaurant.objects.filter(_id=rest_id).first()
        restaurant_categories = cls.get_all_categories(rest_id)
        restaurant_editable = ['categories']
        edit_model(restaurant,
                   {'categories': restaurant_categories},
                   restaurant_editable)
        save_and_clean(restaurant)
        return deleted_food

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """ Retrieves all the PendingFood records a
        PendingRestaurant (given its id by rest_id) is
        associated with

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :raises: ObjectDoesNotExist if the PendingRestaurant of rest_id does not exist
        :raises: MultipleObjectsReturned if there are several records of the given rest_id
        :return: list of PendingFood objects the PendingRestaurant of rest_id
                is associated with
        :rtype: list
        """
        rest_filter = PendingRestaurant.objects.filter(_id=rest_id)
        if not rest_filter.exists():
            raise ObjectDoesNotExist(
                "The PendingRestaurant with _id: " +
                rest_id +
                " does not exist")
        if rest_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one PendingRestaurant with _id: " + rest_id)

        return list(PendingFood.objects.filter(restaurant_id=rest_id))

    @classmethod
    def get_all_categories(cls, rest_id):
        """ Retrieve all categories a restaurant's menu has

        :param rest_id: id of restaurant
        :type rest_id: ObjectId string
        :raises: ObjectDoesNotExist if the PendingRestaurant of rest_id does not exist
        :raises: MultipleObjectsReturned if there are several records of the given rest_id
        :return: list of categories a restaurant's menu has
        :rtype: list
        """
        rest_filter = PendingRestaurant.objects.filter(_id=rest_id)
        if not rest_filter.exists():
            raise ObjectDoesNotExist(
                "The PendingRestaurant with _id: " +
                rest_id +
                " does not exist")
        if rest_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one PendingRestaurant with _id: " + rest_id)

        return list(set(PendingFood.objects.filter(
            restaurant_id=rest_id).values_list('category', flat=True)))

    @classmethod
    def new_category(cls, category, restaurant):
        """
        check if category is new to restaurant
        :param category: restaurant category
        :param restaurant: referenced restaurant
        :return: boolean
        """
        return category not in restaurant.categories

    @classmethod
    def should_add_category(cls, body, category, restaurant):
        """
        check if should add category
        :param body:
        :param category:
        :param restaurant:
        :return:
        """
        return cls.new_category(category, restaurant)

    @classmethod
    def add_category(cls, category, restaurant):
        """
        add new category to restaurant
        :param category:
        :param restaurant:
        :return:
        """
        restaurant.categories.append(category)
        restaurant.save(update_fields=['categories'])

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are any invalid field(s)
        :return: None
        """
        dish_urls = ['picture']
        invalid = {'Invalid': []}

        for field in dish_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    @classmethod
    def upload_media(self, dish, form_data, form_file):
        """ Uploads an image to Google Cloud bucket
        and updates the field in the PendingFood record
        with the link to the uploaded image.
        Deletes the previous image associated with the PendingFood record,
        if the url to the image DOES NOT match the url to the image
        on the Food record (the approved version of the food).

        :param dish: the PendingFood object to be updated
        :type dish: :class: `PendingFood`
        :param form_data: the form containing fields that specify the file,
            and the file type
        :type form_data: QueryDict
        :param form_file: the file(s) to be uploaded
        :type form_file: File
        :return: the updated PendingFood object
        :rtype: :class: `PendingFood`
        """
        media_type = form_data.get('media_type')
        save_location = form_data.get('save_location')
        media_file = form_file['media_file']

        file_path = upload(media_file, IMAGE)

        approved_dish = Food.objects.filter(_id=dish._id).first()
        old_file_path = getattr(dish, save_location)
        if approved_dish:
            approved_file_path = getattr(approved_dish, save_location)
            # Deletes the PendingFood record's previous image
            if approved_file_path != old_file_path:
                delete(old_file_path)
        else:
            delete(old_file_path)

        setattr(dish, save_location, file_path)
        return save_and_clean(dish)


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
    locationNotes = models.CharField(max_length=2000, blank=True, default='')

    web_url = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(max_length=200)
    cover_photo_url = models.CharField(
        max_length=200,
        default='https://storage.googleapis.com/default-assets/cover.jpg')
    logo_url = models.CharField(
        max_length=200,
        default='https://storage.googleapis.com/default-assets/logo.jpg')
    restaurant_video_url = models.CharField(max_length=200, default='/')
    restaurant_image_url = models.TextField(default='["/"]', blank=True)

    owner_first_name = CustomListField(default=[], blank=True)
    owner_last_name = CustomListField(default=[], blank=True)
    owner_preferred_name = CustomListField(default=[], blank=True)

    categories = CustomListField(default=[], blank=True)
    status = models.CharField(
        max_length=200,
        default=Status.Approved.value,
        choices=Status.choices())

    sysAdminComments = models.CharField(
        blank=True, default='', max_length=2000)

    open_hours = models.TextField(default='')
    payment_methods = models.TextField(default='["/"]')

    full_menu_url = models.CharField(max_length=200, blank=True)
    approved_once = models.BooleanField(default=False, blank=True)
    restaurant_video_desc = models.TextField(default='', blank=True)

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
        :return: A boolean representing if a category exists
            in the restaurant's categories field
        :type: boolean
        """
        return category in self.categories

    @classmethod
    def get(cls, _id):
        """ retrieve restaurant based on id

        :param _id: id of restaurant
        :type _id: ObjectId str
        :raises: NotFound if the restaurant with given _id is not found
        :raises: MultipleObjectsReturned if there are more than one
            restaurant of the given _id
        :return: :class: `Restaurant`
        :rtype: :class: `Restaurant`
        """
        restaurant_filter = cls.objects.filter(_id=_id)
        if not restaurant_filter.exists():
            raise NotFound(
                "Cannot find Restaurant with _id: " + _id)
        if restaurant_filter.count() > 1:
            raise MultipleObjectsReturned(
                "Received multiple records of Restaurant with _id: " + _id)
        restaurant = restaurant_filter.first()
        return restaurant


class PendingRestaurant(models.Model):
    """ Model for Restaurants """

    attr_list = [
        'name', 'phone', 'web_url', 'years',
        'address', 'streetAddress2', 'streetAddress3',
        'postalCode', 'owner_first_name', 'owner_last_name',
        'owner_preferred_name',
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
    locationNotes = models.CharField(max_length=2000, blank=True, default='')

    web_url = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True, blank=True)
    GEO_location = models.CharField(max_length=200, blank=True)
    cover_photo_url = models.CharField(
        max_length=200,
        default='https://storage.googleapis.com/default-assets/cover.jpg',
        blank=True)
    logo_url = models.CharField(
        max_length=200,
        default='https://storage.googleapis.com/default-assets/logo.jpg',
        blank=True)
    restaurant_video_url = models.CharField(
        max_length=200, default='/', blank=True)
    restaurant_image_url = models.TextField(default='["/"]', blank=True)

    owner_first_name = CustomListField(default=[], blank=True)
    owner_last_name = CustomListField(default=[], blank=True)
    owner_preferred_name = CustomListField(default=[], blank=True)

    categories = CustomListField(default=[], blank=True)
    status = models.CharField(
        max_length=200,
        default=Status.In_Progress.value,
        choices=Status.choices())

    sysAdminComments = models.CharField(
        blank=True, default='', max_length=2000)

    modified_time = models.DateTimeField(
        editable=False, null=True, default=timezone.now)

    open_hours = models.TextField(default='', blank=True)
    payment_methods = models.TextField(default='["/"]', blank=True)

    full_menu_url = models.CharField(max_length=200, blank=True)
    approved_once = models.BooleanField(default=False, blank=True)
    restaurant_video_desc = models.TextField(default='', blank=True)

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
    def insert(cls, restaurant_data):
        """ Insert pending restaurant into database given restaurant data

        :param restaurant_data: json data of restaurant
        :type restaurant_data: json
        :raises: IntegrityError if the pending restaurant
            already exists in the database
        :return: restaurant object representing sent data
        :rtype: :class:`PendingRestaurant` object
        """
        if cls.objects.filter(email=restaurant_data['email']).exists():
            raise IntegrityError(
                'Cannot insert pending restaurant object, an object with this email already exists')
        if restaurant_data['years'] == 0:
            restaurant_data['years'] = 1
        restaurant = cls(
            **restaurant_data
        )
        address = restaurant_data['address'] + ', ' + \
            restaurant_data['postalCode'] + ', Ontario'
        update_model_geo(restaurant, address)
        restaurant = save_and_clean(restaurant)
        return restaurant

    @classmethod
    def get(cls, _id):
        """ retrieve restaurant based on id

        :param _id: id of restaurant
        :type _id: ObjectId string
        :raises: ObjectDoesNotExist if record of given _id cannot be found
        :raises: MultipleObjectsReturned if there are several records of given _id
        :return: PendingRestaurant record of given _id
        :rtype: :class: `PendingRestaurant`
        """
        restaurant_filter = cls.objects.filter(_id=_id)
        if not restaurant_filter.exists():
            raise NotFound(
                "Cannot find PendingRestaurant with _id: " + _id)
        if restaurant_filter.count() > 1:
            raise MultipleObjectsReturned(
                "Received multiple records of PendingRestaurant with _id: " + _id)
        restaurant = restaurant_filter.first()
        return restaurant

    @classmethod
    def edit_draft(cls, user_id, body):
        """ Edits the PendingRestaurant owned by the user
        of the given user_id and marks the status as 'In_Progress',
        body contains the fields and their updated valus

        :param user_id: id of the restaurant owner user
        :type user_id: int
        :param body: dict containing PendingRestaurant fields
            and the updated values
        :type body: dict
        :raises: ObjectDoesNotExist if the PendingRestaurant
            owned by user_id does not exist
        :return: the updated PendingRestaurant
        :rtype: :class: `PendingRestaurant`
        """
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise ObjectDoesNotExist(
                'restaurant with owner user id ' + str(user_id) + ' does not exist')

        if 'years' in body and body['years'] == 0:
            body['years'] = 1
        body["status"] = Status.In_Progress.value
        body["modified_time"] = timezone.now()
        edit_model(restaurant, body, restaurant_editable)
        if cls.address_changed(body):
            address = restaurant.address + ', ' + restaurant.postalCode + ', Ontario'
            update_model_geo(restaurant, address)
        return save_and_clean(restaurant)

    @classmethod
    def edit_approval(cls, user_id, body):
        """ Edits the PendingRestaurant owned by the user
        of the given user_id and marks the status as 'Pending',
        body contains the fields and their updated valus

        :param user_id: id of the restaurant owner user
        :type user_id: int
        :param body: dict containing PendingRestaurant fields
            and the updated values
        :type body: dict
        :raises: ObjectDoesNotExist if the PendingRestaurant
            owned by user_id does not exist
        :return: the updated PendingRestaurant
        :rtype: :class: `PendingRestaurant`
        """
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise ObjectDoesNotExist(
                'restaurant with owner user id ' + str(user_id) + ' does not exist')

        if 'years' in body and body['years'] == 0:
            body['years'] = 1
        body["status"] = Status.Pending.value
        body["modified_time"] = timezone.now()
        edit_model(restaurant, body, restaurant_editable)
        if cls.address_changed(body):
            address = restaurant.address + ', ' + restaurant.postalCode + ', Ontario'
            update_model_geo(restaurant, address)
        return save_and_clean(restaurant)

    @classmethod
    def address_changed(cls, body):
        """
        return if address has changed
        :param body: edited fields
        :return: boolean
        """
        return 'address' in body

    def category_exists(self, category):
        """ Check whether category is new

        :param category: referenced category
        :type category: string
        :return: A boolean representing if a category exists
            in the restaurant's categories field
        :type: boolean
        """
        return category in self.categories

    @classmethod
    def field_validate_draft(self, fields):
        """ Validates only the required fields for inserting a restaurant draft

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are invalid(s)
        :return: None
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

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    @classmethod
    def field_validate(self, fields):
        """ Validates all fields of a restaurant for admin approval

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are invalid(s)
        :return: None
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
                if len(str(fields['phone'])) != 10 and str(
                        fields['phone']).isnumeric():
                    invalid['Invalid'].append('phone')
            else:
                invalid['Invalid'].append('phone')

        if 'email' in fields:
            try:
                validate_email(fields['email'])
            except ValidationError as e:
                invalid['Invalid'].append('email')

        if 'pricepoint' in fields and not fields['pricepoint']:
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

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")

    @classmethod
    def upload_media(self, restaurant, form_data, form_file):
        """ Uploads an image(s) or video to Google Cloud bucket
        and updates the field in the PendingRestaurant record
        with the link to the uploaded image/video.
        Deletes the previous image associated with the PendingRestaurant record,
        if the url to the image DOES NOT match the url to the image
        on the Restaurant record (the approved version of the restaurant).

        :param restaurant: the PendingRestaurant object to be updated
        :type restaurant: :class: `PendingRestaurant`
        :param form_data: the form containing fields that specify the file,
            the file type, and whether this PendingRestaurant is just created
            or is being edited
        :type form_data: QueryDict
        :param form_file: the file(s) to be uploaded
        :type form_file: File or Array of Files
        :raises: ValidationError upon any invalid field values or violations
            against business logic
        :return: the updated PendingRestaurant object
        :rtype: :class: `PendingRestaurant`
        """
        media_type = form_data.get('media_type')
        save_location = form_data.get('save_location')
        media_link = form_data.get('media_link')
        submit_for_approval = form_data.get('submit_for_approval')

        if media_type == MediaType.IMAGE.name:
            if save_location == 'restaurant_video_url':
                raise ValidationError(
                    message="Invalid save_location for media_type",
                    code="invalid_input")

            if save_location == RestaurantSaveLocations.restaurant_image_url.name:
                media_files_list = form_file.getlist('media_file')
                file_path = ast.literal_eval(restaurant.restaurant_image_url)
                if '/' in file_path:
                    file_path.remove('/')

                for image in media_files_list:
                    file_path.append(upload(image, IMAGE))
                file_path = json.dumps(file_path)
            else:
                media_file = form_file['media_file']
                file_path = upload(media_file, IMAGE)
        else:
            if save_location != 'restaurant_video_url':
                raise ValidationError(
                    message="Invalid save_location for media_type",
                    code="invalid_input")

            if media_link:
                youtube_url_check = re.compile(
                    "^(?:https?:\\/\\/)?(?:m\\.|www\\.)?(?:youtu\\.be\\/|youtube\\.com\\/(?:embed\\/|v\\/|watch\\?v=|watch\\?.+&v=))((\\w|-){11})(?:\\S+)?$")
                if not youtube_url_check.match(media_link):
                    raise ValidationError(
                        message="Invalid YouTube url", code="invalid_input")
                file_path = media_link
            else:
                media_file = form_file['media_file']
                file_path = upload(media_file, VIDEO)

        approved_restaurant = Restaurant.objects.filter(
            _id=restaurant._id).first()
        old_file_path = getattr(restaurant, save_location)
        if submit_for_approval == 'False':
            setattr(restaurant, 'status', Status.In_Progress.value)
        else:
            setattr(restaurant, 'status', Status.Pending.value)
        if approved_restaurant:
            approved_file_path = getattr(approved_restaurant, save_location)
            if save_location != RestaurantSaveLocations.restaurant_image_url.name and approved_file_path != old_file_path:
                delete(old_file_path)
        else:
            delete(old_file_path)

        setattr(restaurant, save_location, file_path)
        return save_and_clean(restaurant)

    @classmethod
    def delete_media(self, restaurant, form_data):
        """ Deletes image(s) from Google Cloud bucket and
        updates the restaurant_image_url field in the PendingRestaurant
        object

        :param restaurant: the PendingRestaurant object to be updated
        :type restaurant: :class: `PendingRestaurant`
        :param form_data: the form containing the list of images to be deleted
        :type form_data: QueryDict
        :return: the updated PendingRestaurant object
        :rtype: :class: `PendingRestaurant`
        """
        restaurant_images = form_data.get('restaurant_images')
        file_path = []
        old_file_path = ast.literal_eval(restaurant.restaurant_image_url)
        for image_url in old_file_path:
            if image_url in restaurant_images:
                delete(image_url)
            else:
                file_path.append(image_url)

        file_path = json.dumps(file_path) if file_path else ['/']
        approved_restaurant = Restaurant.objects.filter(
            _id=restaurant._id).first()
        setattr(restaurant, 'restaurant_image_url', file_path)
        if approved_restaurant:
            setattr(approved_restaurant, 'restaurant_image_url', file_path)
            save_and_clean(approved_restaurant)

        return save_and_clean(restaurant)


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
        :param rest_id: the id of the restaurant for this
            user-restaurant favourite relation
        :type rest_id: ObjectId string
        :raises: ObjectDoesNotExist if the user or restaurant does not exist
        :raises: MultipleObjectsReturned if there are more than one
            user or restaurant with the given ids
        :raises: IntegrityError if the relation already exists
        :return: user-restaurant-favourite relation object with actual restaurant data
            of the favourite restaurant
        :rtype: json object
        """
        user_filter = User.objects.filter(id=user_id)
        restaurant_filter = Restaurant.objects.filter(_id=rest_id)
        user = {}
        restaurant = {}
        if not user_filter.exists():
            ObjectDoesNotExist("The user with user_id: " +
                               str(user_id) + " does not exist")
        if user_filter.count() > 1:
            raise MultipleObjectsReturned(
                'There are more than one user with this user_id')
        user = user_filter.first()

        if not restaurant_filter.filter(_id=rest_id).exists():
            raise ObjectDoesNotExist(
                'The restaurant associated with id ' +
                restaurant_id +
                ' does not exist')
        if restaurant_filter.count() > 1:
            raise MultipleObjectsReturned(
                'There are more than one restaurant with this restaurant_id')
        restaurant = restaurant_filter.first()

        if cls.objects.filter(user_id=user_id, restaurant=rest_id).exists():
            raise IntegrityError(
                'Cannot insert new user-restaurant-favourite relation, this relation already exists')
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
        :raises: ObjectDoesNotExist if one of the restaurants in the list of
            user's favourites does not exist
        :return: list of restaurants in json format
        :rtype: list of json objects
        """
        restaurants = []

        user_filter = User.objects.filter(id=user_id)
        if not user_filter.exists():
            raise ObjectDoesNotExist(
                "The user with user_id: " + str(user_id) + " does not exist")
        if user_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one user with this id: " + str(user_id))

        favourites = UserFavRestrs.objects.filter(user_id=user_id)
        if not favourites:
            return restaurants

        for record in favourites:
            restaurant = Restaurant.objects.filter(
                _id=record.restaurant).first()
            if not restaurant:
                raise ObjectDoesNotExist(
                    'One of the restaurants in the list of favourites does not appear to exist: ' +
                    record.restaurant)
            restaurant.offer_options = ast.literal_eval(
                restaurant.offer_options)
            restaurants.append(model_to_json(restaurant))

        return restaurants

    @classmethod
    def getRestrFavouriteds(cls, restaurant_id):
        """ retrieve all users who have favourited this restaurant
        given the restaurant_id

        :param restaurant_id: id of the restaurant whose list of
            favourited users to retrieve
        :type restaurant_id: ObjectId string
        :raises: ObjectDoesNotExist if the restaurant does not exist,
            or one of the users who favourited this restaurant does not exist
        :return: list of users who favourited this restaurant
        :rtype: list of json objects
        """
        users = []

        if not Restaurant.objects.filter(_id=restaurant_id).exists():
            raise ObjectDoesNotExist(
                'The restaurant associated with id ' +
                restaurant_id +
                ' does not exist')

        favouriteds = UserFavRestrs.objects.filter(restaurant=restaurant_id)
        if not favouriteds:
            return users
        for record in favouriteds:
            user_filter = User.objects.filter(id=record.user_id)
            if not user_filter.exists():
                raise ObjectDoesNotExist(
                    'One of the users in the list of favourites does not appear to exist: ' +
                    record.user)
            user = user_filter.first()
            users.append(model_to_json(user))

        return users

    @classmethod
    def remove_fav(cls, user_id, rest_id):
        """ removes a restaurant from the user's favourites list

        :param user_id: the id of the user whose list of
            favourites will have one restaurant removed
        :type user_id: int
        :param rest_id: the id of the restaurant to be removed
            from the user's list
        :type rest_id: ObjectId string
        :raises: ObjectDoesNotExist if the user does not exist or the
            user-restaurant favourite relation does not exist
        :return: Message with success or raise ObjectDoesNotExist
        :rtype: json object
        """
        user_filter = User.objects.filter(id=user_id)
        if not user_filter.exists():
            raise ObjectDoesNotExist(
                "The user with user_id: " + str(user_id) + " does not exist")

        user_fav_filter = UserFavRestrs.objects.filter(
            user_id=user_id, restaurant=rest_id)
        if not user_fav_filter.exists():
            raise ObjectDoesNotExist(
                "This user-restaurant favourite relation does not exist")

        user_fav_filter.delete()
        response = {
            "message": "Successfully removed restaurant from user's favourites"
        }
        return response

    @classmethod
    def field_validate(self, fields):
        """ Validates fields (user_id and restaurant_id)

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are invalid(s)
        :return: None
        """

        invalid = {'Invalid': []}

        if 'user_id' in fields:
            if fields['user_id']:
                if not str(fields['user_id']).isnumeric():
                    invalid['Invalid'].append('user_id')
            else:
                invalid['Invalid'].append('user_id')

        if 'restaurant' in fields:
            try:
                ObjectId(fields['restaurant'])
            except Exception:
                invalid['Invalid'].append('restaurant')

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")


class RestaurantPost(models.Model):
    """ Model for a restaurant post """
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    owner_user_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(max_length=4096)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self._id)

    @classmethod
    def insert(cls, post_data: dict, request):
        """ Inserts a new post into the database
        and sends an email to all admins containing
        the link to the RestaurantPost change_form
        page on Django admin

        :param post_data: data of the post to be inserted
        :type post_data: dict
        :param request: the request object of the restaurant post
            insert endpoint
        :type request: HttpRequest
        :return: the newly inserted post record
        :rtype: :class: `RestaurantPost`
        """
        post = RestaurantPost(**post_data)
        post = save_and_clean(post)

        rest_id = post_data["restaurant_id"]
        restaurant_name = PendingRestaurant.objects.filter(
            _id=rest_id).first().name
        send_posts_notify_email(post, restaurant_name, request)
        return post

    @classmethod
    def get_by_user_id(cls, user_id):
        """ Retrieves a list of all posts
        posted by a restaurant owner given their user_id

        :param user_id: the user id of the restaurant owner
        :type user_id: int
        :raises ObjectDoesNotExist: when the restaurant owner user does not exist
        :raises MultipleObjectsReturned: when there are more than one restaurant owner
            of the given user_id
        :return: list of post records
        :rtype: list of :class: `RestaurantPost`
        """
        ro_filter = User.objects.filter(id=user_id)
        if not ro_filter.exists:
            raise ObjectDoesNotExist(
                "The restaurant owner with id: " + str(user_id) + " does not exist")
        if ro_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one sduser record for the user with id: " + str(user_id))

        posts = list(RestaurantPost.objects.filter(owner_user_id=user_id))
        response = {"Posts": []}
        for post in posts:
            time_stamp = {
                "Timestamp": post.timestamp.strftime("%b %d, %Y %H:%M")}
            response["Posts"].append(model_to_json(post, time_stamp))
        return response

    @classmethod
    def get_by_rest_id(cls, rest_id):
        """ Retrieves a list of all posts
        posted by a restaurant owner given the restaurant's
        _id

        :param rest_id: the _id of the restaurant
        :type rest_id: ObjectId str
        :raises ObjectDoesNotExist: when the restaurant does not exist
        :raises MultipleObjectsReturned: when there are more than one restaurant
            of the given rest_id
        :return: list of post records
        :rtype: list of :class: `RestaurantPost`
        """
        rest_filter = PendingRestaurant.objects.filter(_id=rest_id)
        if not rest_filter.exists:
            raise ObjectDoesNotExist(
                "The restaurant with _id: " + rest_id + " does not exist")
        if rest_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one restaurant record with _id: " + rest_id)

        posts = list(RestaurantPost.objects.filter(restaurant_id=rest_id))
        response = {"Posts": []}
        for post in posts:
            time_stamp = {
                "Timestamp": post.timestamp.strftime("%b %d, %Y %H:%M")}
            response["Posts"].append(model_to_json(post, time_stamp))
        return response

    @classmethod
    def remove_post(cls, post_id):
        """ Removes a post from the database given
        the post's id

        :param post_id: the id of the post to be deleted
        :type post_id: ObjectId str
        :raises ObjectDoesNotExist: when the post of the given id does not exist
        :raises MultipleObjectsReturned: when there are multiple posts of the given id
        :return: the deleted post record
        :rtype: :class: `RestaurantPost`
        """
        post_filter = RestaurantPost.objects.filter(_id=post_id)
        if not post_filter.exists():
            raise ObjectDoesNotExist(
                "No posts found with this _id: " + post_id)
        if post_filter.count() > 1:
            raise MultipleObjectsReturned(
                "There are more than one post with this _id: " + post_id)

        post = post_filter.first()
        deleted_post = post_filter.first()
        post.delete()
        return deleted_post

    @classmethod
    def field_validate(self, fields):
        """ Validates fields

        :param fields: Dictionary of fields to validate
        :type fields: dict
        :raises: ValidationError when there are invalid(s)
        :return: None
        """

        invalid = {'Invalid': []}

        if 'restaurant_id' in fields:
            try:
                ObjectId(fields['restaurant_id'])
            except Exception:
                invalid['Invalid'].append('restaurant_id')

        if 'content' in fields:
            try:
                if not fields['content']:
                    invalid['Invalid'].append('content')
                else:
                    validate_profane_content(fields['content'])
            except ValidationError:
                invalid['Invalid'].append('content')

        if invalid['Invalid']:
            raise ValidationError(message=invalid, code="invalid_input")
