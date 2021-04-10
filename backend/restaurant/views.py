from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, QueryDict
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate

from restaurant.enum import Status, MediaType, RestaurantSaveLocations, FoodSaveLocations
from restaurant.models import (
    Food,
    Restaurant,
    PendingRestaurant,
    PendingFood,
    UserFavRestrs,
    RestaurantPost
)
from restaurant.forms import RestaurantMediaForm, RestaurantImageDeleteForm, FoodMediaForm

from google.analytics import get_access_token, get_analytics_data

from utils.model_util import model_to_json, save_and_clean, edit_model, update_model_geo, models_to_json
from utils.permissions import ROPermission

from bson import ObjectId
import ast
import json

# jsonschema validation schemas for request bodies
food_insert_schema = {
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": ["string", "number"]},
        "specials": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["name", "description", "price", "specials", "category"],
    "additionalProperties": False
}

food_edit_schema = {
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": ["string", "number"]},
        "specials": {"type": "string"},
        "category": {"type": "string"}
    },
    "additionalProperties": False
}

food_delete_schema = {
    "properties": {
        "name": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["name", "category"],
    "additionalProperties": False
}

restaurant_insert_for_approval_schema = {
    "properties": {
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "GEO_location": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"}
    },
    "required": ["name", "years", "address", "postalCode", "phone", "pricepoint", "offer_options",
                 "bio", "owner_first_name", "owner_last_name", "open_hours", "payment_methods"],
    "additionalProperties": False
}

restaurant_insert_draft_schema = {
    "properties": {
        "restaurant_id": {"type": "string"},
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"}
    },
    "required": ["name", "address", "postalCode", "owner_first_name", "owner_last_name"],
    "additionalProperties": False
}

restaurant_edit_draft_schema = {
    "properties": {
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"}
    },
    "required": ["name", "address", "postalCode", "owner_first_name", "owner_last_name"],
    "additionalProperties": False
}

user_fav_schema = {
    "properties": {
        "restaurant": {"type": "string"}
    },
    "required": ["restaurant"],
    "additionalProperties": False
}

post_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}


class DishList(APIView):
    """ dish list """
    permission_classes = (AllowAny,)

    def get(self, request):
        """ Retrieve all dishes from the database """
        foods = Food.objects.all()
        response = {'Dishes': models_to_json(foods)}
        return JsonResponse(response)


class DishRestaurantView(APIView):
    """ dish restaurant view """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """ Retrieve all dishes from a restaurant """
        dishes = Food.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)


class PendingDishView(APIView):
    """ pending dish view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def get(self, request):
        """Retrieve all dishes from a restaurant"""
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "The restaurant with owner_user_id: " +
                user_id +
                " does not exist")
        rest_id = restaurant._id
        dishes = PendingFood.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)

    def post(self, request):
        """ Insert dish into database """
        user = request.user
        if not user:
            raise PermissionDenied(
                detail="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data, schema=food_insert_schema)
        body = request.data
        PendingFood.field_validate(body)

        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "The restaurant with owner_user_id: " +
                user_id +
                " does not exist")

        rest_id = restaurant._id
        food = PendingFood.add_dish(body, rest_id)
        return JsonResponse(model_to_json(food))

    def put(self, request, dish_id):
        """ Update Dish data """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data,
                 schema=food_edit_schema)
        body = request.data
        PendingFood.field_validate(body)

        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "The restaurant with owner_user_id: " +
                user_id +
                " does not exist")

        rest_id = restaurant._id
        dish = PendingFood.edit_dish(dish_id, body, rest_id)
        return JsonResponse(model_to_json(dish))

    def delete(self, request):
        """ Deletes dish from database """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data, schema=food_delete_schema)
        body = request.data
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "The restaurant with owner_user_id: " +
                user_id +
                " does not exist")
        deleted_dish = PendingFood.remove_dish(body, restaurant._id)
        return JsonResponse(model_to_json(deleted_dish))


def remove_category(category, restaurant):
    """
    remove category from restaurant
    :param category: food category
    :param restaurant: restaurant document
    """
    restaurant.categories.remove(category)
    restaurant.save(update_fields=['categories'])


def category_exists(restaurant_id, category):
    """
    check if restaurant still covers category 'category'
    :param restaurant:referenced restaurant
    :param category: category
    :return:boolean
    """
    return PendingFood.objects.filter(
        restaurant_id=restaurant_id,
        category=category).exists()


# get_user_favs_page
# add_user_fav_page
class UserFavView(APIView):
    """ user fav view """
    #permission_classes = (AllowAny,)
    #permission_classes = [ROPermission]

    def post(self, request):
        """ Add a new user-restaurant-favourite relation """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data, schema=user_fav_schema)
        body = request.data
        body['user_id'] = user_id
        rest_id = body['restaurant']
        UserFavRestrs.field_validate(body)
        response = UserFavRestrs.insert(user_id, rest_id)
        return JsonResponse(response, safe=False)

    def get(self, request):
        """ Get all restaurants favourited by a user """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        response = UserFavRestrs.getUserFavourites(user_id)
        return JsonResponse(response, safe=False)


class UserFavRestaurantView(APIView):
    """ user fav restaurants view """
    #permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """ Get all users who favourited the requested restaurant """
        response = UserFavRestrs.getRestrFavouriteds(rest_id)
        return JsonResponse(response, safe=False)


class FavRelationView(APIView):
    """ remove fav relation view """
    #permission_classes = (AllowAny,)

    def delete(self, request, rest_id):
        """ Remove a new user-restaurant-favourite relation """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        body = {'user_id': user_id, 'restaurant_id': rest_id}
        UserFavRestrs.field_validate(body)
        response = UserFavRestrs.remove_fav(user_id, rest_id)
        return JsonResponse(response, safe=False)


class RestaurantView(APIView):
    """ get restaurant view """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """ Retrieve approved restaurant by id """
        restaurant = Restaurant.get(rest_id)
        restaurant_image_url = ast.literal_eval(
            restaurant.restaurant_image_url)
        offer_options = ast.literal_eval(restaurant.offer_options)
        payment_methods = ast.literal_eval(restaurant.payment_methods)

        restaurant = model_to_json(restaurant)
        restaurant['restaurant_image_url'] = restaurant_image_url
        restaurant['offer_options'] = offer_options
        restaurant['payment_methods'] = payment_methods
        return JsonResponse(restaurant)


class PendingRestaurantView(APIView):
    """ pending restaurant view """
    permission_classes = [ROPermission]

    def get(self, request):
        """ Retrieve restaurant from pending collection by the owner's user_id """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise ObjectDoesNotExist(
                'No pending restaurant found with owner user id of this: ' + _id)

        restaurant_image_url = ast.literal_eval(
            restaurant.restaurant_image_url)
        offer_options = ast.literal_eval(restaurant.offer_options)
        payment_methods = ast.literal_eval(restaurant.payment_methods)

        restaurant = model_to_json(restaurant)
        restaurant['restaurant_image_url'] = restaurant_image_url
        restaurant['offer_options'] = offer_options
        restaurant['payment_methods'] = payment_methods
        return JsonResponse(restaurant)


class AllRestaurantList(APIView):
    """ all restaurants list """
    permission_classes = (AllowAny,)

    def get(self, request):
        """Retrieve all restaurants"""
        restaurants = models_to_json(list(Restaurant.objects.all()))
        for restaurant in restaurants:
            restaurant['restaurant_image_url'] = ast.literal_eval(
                restaurant['restaurant_image_url'])
            restaurant['offer_options'] = ast.literal_eval(
                restaurant['offer_options'])
            restaurant['payment_methods'] = ast.literal_eval(
                restaurant['payment_methods'])
        response = {'Restaurants': restaurants}
        return JsonResponse(response)


class RestaurantDraftView(APIView):
    """ insert restaurant draft view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def post(self, request):
        """ Insert new restaurant as a draft into database """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        validate(instance=request.data,
                 schema=restaurant_insert_draft_schema)
        body = request.data
        PendingRestaurant.field_validate_draft(body)
        restaurant = PendingRestaurant.insert(body)
        return JsonResponse(model_to_json(restaurant))

    def put(self, request):
        """ Edit a restaurant profile and save it as a draft in the database """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data,
                 schema=restaurant_edit_draft_schema)
        body = request.data
        PendingRestaurant.field_validate_draft(body)
        restaurant = PendingRestaurant.edit_draft(user_id, body)
        return JsonResponse(model_to_json(restaurant))


class RestaurantForApprovalView(APIView):
    """ inser restaurant for approval view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def put(self, request):
        """ Insert or update a restaurant record for admin approval """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data,
                 schema=restaurant_insert_for_approval_schema)
        body = request.data
        PendingRestaurant.field_validate(body)

        rest_filter = PendingRestaurant.objects.filter(owner_user_id=user_id)
        if not rest_filter.exists():
            body['status'] = Status.Pending.value
            restaurant = PendingRestaurant.insert(body)
        else:
            restaurant = PendingRestaurant.edit_approval(user_id, body)
        return JsonResponse(model_to_json(restaurant))


def category_is_changed(body):
    """
    check whether category was edited
    :param body: request body for editing
    :return: boolean
    """
    return 'category' in body


class AnalyticsAccessTokenView(APIView):
    """ analytics access token view """

    def get(self, request):
        """ Get OAuth2 access token for Google Analytics API to make call """
        return JsonResponse({'token': get_access_token()})


class RestaurantAnalyticsDataView(APIView):
    """ analytics data view """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id, format_type):
        """ Retrieves analytics data for a specific restaurant page
        given restaurant id and format of date """
        restaurant = Restaurant.objects.get(_id=rest_id)
        traffic = get_analytics_data(rest_id, format_type)
        traffic['name'] = restaurant.name
        return JsonResponse(traffic)


class RestaurantsAnalyticsDataView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format_type):
        """ Retrieves analytics data for all restaurants page
        given their restaurant ids and format of date """
        restaurants = list(Restaurant.objects.all())
        restaurant_data = {}
        for restaurant in restaurants:
            restJson = model_to_json(restaurant)
            rest_id = restJson.get('_id')
            traffic = get_analytics_data(rest_id, format_type)
            traffic['name'] = restJson.get('name')
            restaurant_data[rest_id] = traffic
        return JsonResponse(restaurant_data)


class PostView(APIView):
    """ Restaurant posts view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def post(self, request):
        """ Insert a new post for a restaurant """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        validate(instance=request.data, schema=post_schema)
        body = request.data
        body['owner_user_id'] = user_id
        RestaurantPost.field_validate(body)

        post = RestaurantPost.insert(body, request)
        return JsonResponse(model_to_json(post))

    def get(self, request):
        """ Get all posts for a restaurant """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")
        user_id = user.id
        posts = RestaurantPost.get_by_user_id(user_id)
        return JsonResponse(posts)

    def delete(self, request, post_id):
        """ Deletes a single restaurant post """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")
        post_deleted = RestaurantPost.remove_post(post_id)
        return JsonResponse({"Deleted post": model_to_json(post_deleted)})


class PublicPostView(APIView):
    """ Restaurant posts view for all viewers """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """ Get all posts for a restaurant """
        posts = RestaurantPost.get_by_rest_id(rest_id)
        return JsonResponse(posts)


class RestaurantMediaView(APIView):
    """ Restaurant media (image/video) view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def put(self, request):
        """ For inserting or updating restaurant media """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "Could not find restaurant owned by this user")

        form = RestaurantMediaForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        restaurant = PendingRestaurant.upload_media(
            restaurant, request.data, request.FILES)
        return JsonResponse(model_to_json(restaurant))

    def delete(self, request):
        """ For removing image(s) from the restaurant_image_url field
        and Google Cloud bucket """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        restaurant = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()
        if not restaurant:
            raise IntegrityError(
                "Could not find restaurant owned by this user")

        form = RestaurantImageDeleteForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        restaurant = PendingRestaurant.delete_media(restaurant, request.data)
        return JsonResponse(model_to_json(restaurant))


class DishMediaView(APIView):
    """ Dish media (image) view """
    #permission_classes = (AllowAny,)
    permission_classes = [ROPermission]

    def put(self, request, dish_id):
        """ For inserting or updating restaurant media """
        user = request.user
        if not user:
            raise PermissionDenied(
                message="Failed to obtain user",
                code="fail_obtain_user")

        user_id = user.id
        dish = PendingFood.objects.filter(_id=dish_id).first()
        if not dish:
            raise IntegrityError("Could not find the dish with id: " + dish_id)

        form = FoodMediaForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        dish = PendingFood.upload_media(dish, request.data, request.FILES)
        return JsonResponse(model_to_json(dish))
