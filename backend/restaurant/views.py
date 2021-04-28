from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, QueryDict
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from sduser.backends import check_user_status
from restaurant import schemas
from restaurant.forms import RestaurantMediaForm, RestaurantImageDeleteForm, FoodMediaForm
from restaurant.enum import Status, MediaType, RestaurantSaveLocations, FoodSaveLocations
from restaurant.models import (
    Food,
    Restaurant,
    PendingRestaurant,
    PendingFood,
    UserFavRestrs,
    RestaurantPost
)
from google.analytics import get_analytics_data
from utils.model_util import model_to_json, save_and_clean, edit_model, update_model_geo, models_to_json
from utils.permissions import ROPermission
from utils.geo_controller import reverse_geocode

from jsonschema import validate
from bson import ObjectId
import ast
import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from restaurant import swagger


class DishList(APIView):
    """ dish list """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.dish_all_response,
                         operation_id="GET /dish/all/")
    def get(self, request):
        """ Retrieve all dishes from the database """
        foods = Food.objects.all()
        response = {'Dishes': models_to_json(foods)}
        return JsonResponse(response)


class DishRestaurantView(APIView):
    """ dish restaurant view """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.dish_approved_rest_id_response,
                         operation_id="GET /dish/approved/{rest_id}/")
    def get(self, request, rest_id):
        """ Retrieve all approved dishes from a restaurant """
        dishes = Food.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)


class PendingDishView(APIView):
    """ pending dish view """
    permission_classes = [ROPermission]

    @swagger_auto_schema(responses=swagger.dish_pending_get_response,
                         operation_id="GET /dish/pending/")
    def get(self, request):
        """ Retrieve all dishes from restaurant owned by user """
        user = request.user
        check_user_status(user)

        user_id = user.id
        restaurant = PendingRestaurant.get_by_owner(user_id)
        rest_id = restaurant._id
        dishes = PendingFood.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)

    @swagger_auto_schema(request_body=swagger.PendingFoodInsertUpdate,
                         responses=swagger.dish_pending_post_response,
                         operation_id="POST /dish/pending/")
    def post(self, request):
        """ Insert dish into database """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data, schema=schemas.food_insert_edit_schema)
        body = request.data
        PendingFood.field_validate(body)

        restaurant = PendingRestaurant.get_by_owner(user_id)

        rest_id = restaurant._id
        food = PendingFood.add_dish(body, rest_id)
        return JsonResponse(model_to_json(food))


class PendingDishModifyDeleteView(APIView):
    """ PendingDish view for updating or deleting """
    permission_classes = [ROPermission]

    @swagger_auto_schema(request_body=swagger.PendingFoodInsertUpdate,
                         responses=swagger.dish_pending_dish_id_put_response,
                         operation_id="PUT /dish/pending/{dish_id}/")
    def put(self, request, dish_id):
        """ Updates dish data """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data,
                 schema=schemas.food_insert_edit_schema)
        body = request.data
        PendingFood.field_validate(body)

        restaurant = PendingRestaurant.get_by_owner(user_id)

        dish = PendingFood.edit_dish(dish_id, body, restaurant._id)
        return JsonResponse(model_to_json(dish))

    @swagger_auto_schema(responses=swagger.dish_pending_dish_id_delete_response,
                         operation_id="DELETE /dish/pending/{dish_id}/")
    def delete(self, request, dish_id):
        """ Deletes dish from database """
        user = request.user
        check_user_status(user)

        user_id = user.id
        restaurant = PendingRestaurant.get_by_owner(user_id)
        deleted_dish = PendingFood.remove_dish(dish_id, restaurant._id)
        return JsonResponse(model_to_json(deleted_dish))


# get_user_favs_page
# add_user_fav_page
class UserFavView(APIView):
    """ user fav view """

    @swagger_auto_schema(request_body=swagger.UserFavRest,
                         responses=swagger.user_favourite_post_response,
                         operation_id="POST /user/favourite/")
    def post(self, request):
        """ Add a new user-restaurant-favourite relation """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data, schema=schemas.user_fav_schema)
        body = request.data
        body['user_id'] = user_id
        rest_id = body['restaurant']
        UserFavRestrs.field_validate(body)
        response = UserFavRestrs.insert(user_id, rest_id)
        return JsonResponse(response, safe=False)

    @swagger_auto_schema(responses=swagger.user_favourite_get_response,
                         operation_id="GET /user/favourite/")
    def get(self, request):
        """ Get all restaurants favourited by a user """
        user = request.user
        check_user_status(user)

        user_id = user.id
        response = UserFavRestrs.getUserFavourites(user_id)
        return JsonResponse(response, safe=False)


class UserFavRestaurantView(APIView):
    """ user fav restaurants view """

    @swagger_auto_schema(
        responses=swagger.restaurant_rest_id_favourited_users_get_response,
        operation_id="GET /restaurant/{rest_id}/favourited_users/")
    def get(self, request, rest_id):
        """ Get all users who favourited the requested restaurant """
        response = UserFavRestrs.getRestrFavouriteds(rest_id)
        return JsonResponse(response, safe=False)


class FavRelationView(APIView):
    """ remove fav relation view """

    @swagger_auto_schema(
        responses=swagger.user_favourited_rest_id_delete_response,
        operation_id="DELETE /user/favourite/{rest_id}/")
    def delete(self, request, rest_id):
        """ Remove a new user-restaurant-favourite relation """
        user = request.user
        check_user_status(user)

        user_id = user.id
        body = {'user_id': user_id, 'restaurant_id': rest_id}
        UserFavRestrs.field_validate(body)
        response = UserFavRestrs.remove_fav(user_id, rest_id)
        return JsonResponse(response, safe=False)


class RestaurantView(APIView):
    """ get restaurant view """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses=swagger.restaurant_approved_rest_id_get_response,
        operation_id="GET /restaurant/approved/{rest_id}/")
    def get(self, request, rest_id):
        """ Retrieve approved restaurant by id """
        restaurant = Restaurant.get(rest_id)
        restaurant = model_to_json(restaurant)
        return JsonResponse(restaurant)


class PendingRestaurantView(APIView):
    """ pending restaurant view """
    permission_classes = [ROPermission]

    @swagger_auto_schema(responses=swagger.restaurant_pending_get_response,
                         operation_id="GET /restaurant/pending/")
    def get(self, request):
        """ Retrieve restaurant from pending collection by the owner's user_id """
        user = request.user
        check_user_status(user)

        user_id = user.id
        restaurant = PendingRestaurant.get_by_owner(user_id)

        restaurant = model_to_json(restaurant)
        return JsonResponse(restaurant)


class AllRestaurantList(APIView):
    """ all restaurants list """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.restaurant_all_get_response,
                         operation_id="GET /restaurant/all/")
    def get(self, request):
        """ Retrieve all approved restaurants """
        restaurants = models_to_json(list(Restaurant.objects.all()))
        response = {'Restaurants': restaurants}
        return JsonResponse(response)


class RestaurantDraftView(APIView):
    """ insert restaurant draft view """
    permission_classes = [ROPermission]

    @swagger_auto_schema(request_body=swagger.PendingRestaurantDraftInsertUpdate,
                         responses=swagger.restaurant_draft_post_response,
                         operation_id="POST /restaurant/draft/")
    def post(self, request):
        """ Insert new restaurant as a draft into database """
        user = request.user
        check_user_status(user)

        validate(instance=request.data,
                 schema=schemas.restaurant_insert_draft_schema)
        body = request.data
        PendingRestaurant.field_validate_draft(body)
        restaurant = PendingRestaurant.insert(body)
        return JsonResponse(model_to_json(restaurant))

    @swagger_auto_schema(request_body=swagger.PendingRestaurantDraftInsertUpdate,
                         responses=swagger.restaurant_draft_put_response,
                         operation_id="PUT /restaurant/draft/")
    def put(self, request):
        """ Edit a restaurant profile and save it as a draft in the database """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data,
                 schema=schemas.restaurant_edit_draft_schema)
        body = request.data
        PendingRestaurant.field_validate_draft(body)
        restaurant = PendingRestaurant.edit_draft(user_id, body)
        return JsonResponse(model_to_json(restaurant))


class RestaurantForApprovalView(APIView):
    """ inser restaurant for approval view """
    permission_classes = [ROPermission]

    @swagger_auto_schema(request_body=swagger.PendingRestaurantSubmit,
                         responses=swagger.restaurant_submit_put_response,
                         operation_id="PUT /restaurant/submit/")
    def put(self, request):
        """ Insert or update a restaurant record for admin approval """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data,
                 schema=schemas.restaurant_insert_for_approval_schema)
        body = request.data
        PendingRestaurant.field_validate(body)

        rest_filter = PendingRestaurant.objects.filter(owner_user_id=user_id)
        if not rest_filter.exists():
            body['status'] = Status.Pending.value
            restaurant = PendingRestaurant.insert(body)
        else:
            restaurant = PendingRestaurant.edit_approval(user_id, body)
        return JsonResponse(model_to_json(restaurant))


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
    permission_classes = [ROPermission]

    @swagger_auto_schema(request_body=swagger.RestaurantPostInsert,
                         responses=swagger.restaurant_post_post_response,
                         operation_id="POST /restaurant/post/")
    def post(self, request):
        """ Insert a new post for a restaurant """
        user = request.user
        check_user_status(user)

        user_id = user.id
        validate(instance=request.data, schema=schemas.post_schema)
        body = request.data
        body['owner_user_id'] = user_id
        RestaurantPost.field_validate(body)

        post = RestaurantPost.insert(body, request)
        return JsonResponse(model_to_json(post))

    @swagger_auto_schema(responses=swagger.restaurant_post_get_response,
                         operation_id="GET /restaurant/post/")
    def get(self, request):
        """ Get all posts for a restaurant (for ROs) """
        user = request.user
        check_user_status(user)

        user_id = user.id
        posts = RestaurantPost.get_by_user_id(user_id)
        return JsonResponse(posts)


class PostDeleteView(APIView):
    """ Restaurant post delete view """

    @swagger_auto_schema(
        responses=swagger.restaurant_post_post_id_delete_response,
        operation_id="DELETE /restaurant/post/{post_id}/")
    def delete(self, request, post_id):
        """ Deletes a single restaurant post """
        user = request.user
        check_user_status(user)

        post_deleted = RestaurantPost.remove_post(post_id)
        return JsonResponse({"Deleted post": model_to_json(post_deleted)})


class PublicPostView(APIView):
    """ Restaurant posts view for all viewers """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.restaurant_post_get_response,
                         operation_id="GET /restaurant/public/post/{rest_id}/")
    def get(self, request, rest_id):
        """ Get all posts for a restaurant given
        restaurant id (for all users) """
        posts = RestaurantPost.get_by_rest_id(rest_id)
        return JsonResponse(posts)


class RestaurantMediaView(APIView):
    """ Restaurant media (image/video) view """
    permission_classes = [ROPermission]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(manual_parameters=swagger.restaurant_media_put_request,
                         responses=swagger.restaurant_media_put_response,
                         operation_id="PUT /restaurant/media/")
    def put(self, request):
        """ For inserting or updating restaurant media """
        user = request.user
        check_user_status(user)

        user_id = user.id
        restaurant = PendingRestaurant.get_by_owner(user_id)

        form = RestaurantMediaForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        restaurant = PendingRestaurant.upload_media(
            restaurant, request.data, request.FILES)
        return JsonResponse(model_to_json(restaurant))

    @swagger_auto_schema(manual_parameters=swagger.restaurant_media_delete_request,
                         responses=swagger.restaurant_media_delete_response,
                         operation_id="DELETE /restaurant/media/")
    def delete(self, request):
        """ For removing image(s) from the restaurant_image_url field
        and Google Cloud bucket """
        user = request.user
        check_user_status(user)

        user_id = user.id
        restaurant = PendingRestaurant.get_by_owner(user_id)

        form = RestaurantImageDeleteForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        restaurant = PendingRestaurant.delete_media(restaurant, request.data)
        return JsonResponse(model_to_json(restaurant))


class DishMediaView(APIView):
    """ Dish media (image) view """
    permission_classes = [ROPermission]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(manual_parameters=swagger.dish_media_put_request,
                         responses=swagger.dish_media_put_response,
                         operation_id="PUT /dish/media/{dish_id}/")
    def put(self, request, dish_id):
        """ For inserting or updating restaurant media """
        user = request.user
        check_user_status(user)

        user_id = user.id
        dish = PendingFood.objects.filter(_id=dish_id).first()
        if not dish:
            raise IntegrityError("Could not find the dish with id: " + dish_id)

        form = FoodMediaForm(request.data, request.FILES)
        if not form.is_valid():
            raise ValidationError(message=form.errors, code="invalid_input")

        dish = PendingFood.upload_media(dish, request.data, request.FILES)
        return JsonResponse(model_to_json(dish))


class ReverseGeocodeView(APIView):
    """ Retrieve address from coordinates (of restaurant) """
    permission_classes = [AllowAny]

    def get(self, request):
        """ For reverse geocoding the lat lng coordinates """
        lat = request.GET['lat']
        lng = request.GET['lng']
        address = reverse_geocode((lat, lng))
        return JsonResponse({'address': address})
