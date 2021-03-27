from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, QueryDict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate
from jsonschema.exceptions import ValidationError

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
from utils.common import get_user

from bson import ObjectId
import ast
import json

# jsonschema validation schemes

food_schema = {
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
        "owner_story": {"type": "string"},
        "owner_picture_url": {"type": "string"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"}
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
        "GEO_location": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},
        "owner_story": {"type": "string"},
        "owner_picture_url": {"type": "string"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"}
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
        "GEO_location": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},
        "owner_story": {"type": "string"},
        "owner_picture_url": {"type": "string"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"}
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


dish_editable = ["name", "description", "picture",
    "price", "specials", "category", "status"]

restaurant_editable = [
    "name", "years", "address", "streetAddress2", "streetAddress3", "postalCode",
    "phone", "updated_at", "cuisines", "pricepoint",
    "offer_options", "deliveryDetails", "locationNotes", "dineinPickupDetails",
    "web_url", "facebook", "twitter", "instagram",
    "bio", "cover_photo_url", "logo_url", "restaurant_video_url", "restaurant_image_url",
    "owner_first_name", "owner_last_name", "owner_preferred_name",
    "owner_story", "owner_picture_url",
    "status", "modified_time", "sysAdminComments",
    "open_hours", "payment_methods", "full_menu_url"
]


class DishList(APIView):
    """ dish list """
    permission_classes = (AllowAny,)

    def get(self, request):
        """Retrieve all dishes from the database"""
        foods = Food.objects.all()
        response = {'Dishes': models_to_json(foods)}
        return JsonResponse(response)


class DishRestaurantView(APIView):
    """ dish restaurant view """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """Retrieve all dishes from a restaurant"""
        # rest_id = request.GET.get('restaurant_id')
        dishes = Food.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)


class PendingDishView(APIView):
    """ pending dish view """
    #permission_classes = (AllowAny,)

    def get(self, request):
        """Retrieve all dishes from a restaurant"""
        user = get_user(request)
        if not user:
            return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
        user_id = user['user_id']

        restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
        if not restaurant:
            return JsonResponse({"message": "The restaurant with owner_user_id: "+user_id+" does not exist"}, status=400)
        rest_id = restaurant._id
        dishes = PendingFood.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)

    def post(self, request, dish_id=''):
        """ Insert dish into database """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data, schema=food_schema)
            body = request.data
            invalid = PendingFood.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({"message": "The restaurant with owner_user_id: "+user_id+" does not exist"}, status=400)
            rest_id = restaurant._id

            if PendingFood.objects.filter(restaurant_id=rest_id, category='Popular Dish').count() == 6 and body['category'] == 'Popular Dish':
                return JsonResponse({'message': 'You can only have up to a maximum of 6 popular dishes.'}, status=400)
            if PendingFood.objects.filter(restaurant_id=rest_id, category='Signature Dish').count() == 1 and body['category'] == 'Signature Dish':
                return JsonResponse({'message': 'You can only have 1 signature dish.'}, status=400)

            food = PendingFood.add_dish(body, rest_id)
            return JsonResponse(model_to_json(food))
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def put(self, request, dish_id):
        """ Update Dish data """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data,
                     schema=food_edit_schema)
            body = request.data
            invalid = PendingFood.field_validate(body)
            if invalid is not None:
                return JsonResponse(invalid)

            dish = PendingFood.objects.filter(_id=dish_id).first()
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({"message": "The restaurant with owner_user_id: "+user_id+" does not exist"}, status=400)
            rest_id = restaurant._id
            if should_add_category(body, dish.category, restaurant):
                add_cateogory(dish.category, restaurant)

            restaurant_editable = ["status"]
            restaurant_editable_values = {'status': Status.In_Progress.value}

            if 'category' in body and PendingFood.objects.filter(restaurant_id=rest_id, category=body['category']).exists():
                if (body['category'] == 'Popular Dish' and PendingFood.objects.filter(restaurant_id=rest_id, category='Popular Dish').count() == 6):
                    if ObjectId(dish_id) not in list(PendingFood.objects.filter(restaurant_id=rest_id, category='Popular Dish').values_list('_id', flat=True)):
                        return JsonResponse({'message': 'You can only have up to a maximum of 6 popular dishes.'}, status=400)
                if (body['category'] == 'Signature Dish' and PendingFood.objects.filter(restaurant_id=rest_id, category='Signature Dish').count() == 1):
                    if dish_id != str(PendingFood.objects.filter(restaurant_id=rest_id, category='Signature Dish').first()._id):
                        return JsonResponse({'message': 'You can only have 1 signature dish.'}, status=400)
                restaurant_editable.append("categories")

            body["status"] = Status.Pending.value
            edit_model(dish, body, dish_editable)
            updated_fields = [field for field in body.keys()]
            dish = save_and_clean(dish, updated_fields)

            if 'categories' in restaurant_editable:
                restaurant_editable_values['categories'] = PendingFood.get_all_categories(
                    restaurant._id)
            edit_model(restaurant, restaurant_editable_values,
                       restaurant_editable)
            save_and_clean(restaurant)
            return JsonResponse(model_to_json(dish))
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def delete(self, request):
        """ Deletes dish from database """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data, schema=food_delete_schema)
            body = request.data
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({"message": "The restaurant with owner_user_id: "+user_id+" does not exist"}, status=400)
            rest_id = restaurant._id
            food = PendingFood.objects.get(
                name=body["name"], category=body['category'], restaurant_id=rest_id)
            food.delete()
            Food.objects.filter(
                name=body['name'], category=body['category'], restaurant_id=rest_id).delete()
            restaurant = PendingRestaurant.objects.get(_id=rest_id)

            restaurant_categories = PendingFood.get_all_categories(rest_id)
            restaurant_editable = ['categories']
            edit_model(restaurant, {'categories': restaurant_categories}, [
                       'categories'])
            save_and_clean(restaurant)
            return JsonResponse({'message': 'Successfully removed dish from restaurant'})
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ObjectDoesNotExist as e:
            return JsonResponse({'message': e.message}, status=404)
        except Exception:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)


def remove_category(category, restaurant):
    """
    remove category from restaurant
    @param category: food category
    @param restaurant: restaurant document
    """
    restaurant.categories.remove(category)
    restaurant.save(update_fields=['categories'])


def category_exists(restaurant_id, category):
    """
    check if restaurant still covers category 'category'
    @param restaurant:referenced restaurant
    @param category: category
    @return:boolean
    """
    return PendingFood.objects.filter(restaurant_id=restaurant_id, category=category).exists()


# get_user_favs_page
# add_user_fav_page
class UserFavView(APIView):
    """ user fav view """
    #permission_classes = (AllowAny,)

    def post(self, request):
        """ Add a new user-restaurant-favourite relation """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data, schema=user_fav_schema)
            body = request.data
            body['user_id'] = user_id
            rest_id = body['restaurant']
            invalid = UserFavRestrs.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            response = UserFavRestrs.insert(user_id, rest_id)
            return JsonResponse(response, safe=False)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            UserFavRestrs.objects.filter(
                user=user_id, restaurant=body['restaurant_id']).delete()
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

    def get(self, request):
        """ Get all restaurants favourited by a user """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            response = UserFavRestrs.getUserFavourites(user_id)
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

# get_user_favs_restr_page

class UserFavRestaurantView(APIView):
    """ user fav restaurants view """
    #permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """ Get all users who favourited the requested restaurant """
        try:
            response = UserFavRestrs.getRestrFavouriteds(rest_id)
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

# remove_fav_page

class FavRelationView(APIView):
    """ remove fav relation view """
    #permission_classes = (AllowAny,)

    def delete(self, request, rest_id):
        """ Remove a new user-restaurant-favourite relation """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            body = {'user_id': user_id, 'restaurant_id': rest_id}
            invalid = UserFavRestrs.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            response = UserFavRestrs.remove_fav(user_id, rest_id)
            return JsonResponse(response, safe=False)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)


class RestaurantView(APIView):
    """ get restaurant view dish view """
    permission_classes = (AllowAny,)

    def get(self, request, rest_id):
        """Retrieve restaurant by id"""
        try:
            # _id = request.GET.get('_id')
            _id = rest_id
            if _id is None:
                return JsonResponse({'message': '_id parameter is required and cannot be None'}, status=400)

            restaurant = Restaurant.get(_id)
            if restaurant:
                restaurant_image_url = ast.literal_eval(
                    restaurant.restaurant_image_url)
                offer_options = ast.literal_eval(restaurant.offer_options)
                payment_methods = ast.literal_eval(restaurant.payment_methods)

                restaurant = model_to_json(restaurant)
                restaurant['restaurant_image_url'] = restaurant_image_url
                restaurant['offer_options'] = offer_options
                restaurant['payment_methods'] = payment_methods
                return JsonResponse(restaurant)
            else:
                return JsonResponse({'message': 'No restaurant found with this id: '+_id}, status=404)
        except Exception:
            return JsonResponse({'message': 'Something went wrong'}, status=500)

# get_pending_restaurant_page

class PendingRestaurantView(APIView):
    """ pending restaurant view """

    def get(self, request):
        """ Retrieve restaurant from pending collection by the owner's user_id """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if restaurant:
                restaurant_image_url = ast.literal_eval(
                    restaurant.restaurant_image_url)
                offer_options = ast.literal_eval(restaurant.offer_options)
                payment_methods = ast.literal_eval(restaurant.payment_methods)

                restaurant = model_to_json(restaurant)
                restaurant['restaurant_image_url'] = restaurant_image_url
                restaurant['offer_options'] = offer_options
                restaurant['payment_methods'] = payment_methods
                return JsonResponse(restaurant)
            else:
                return JsonResponse({'message': 'No pending restaurant found with owner user id of this: '+_id}, status=404)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

# get_all_restaurants_page

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

# insert_restaurant_draft_page

class RestaurantDraftView(APIView):
    """ insert restaurant draft view """
    #permission_classes = (AllowAny,)

    def post(self, request):
        """Insert new restaurant as a draft into database"""
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)

            validate(instance=request.data,
                     schema=restaurant_insert_draft_schema)
            body = request.data
            invalid = PendingRestaurant.field_validate_draft(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            restaurant = model_to_json(PendingRestaurant.insert(body))
            restaurant['restaurant_image_url'] = ast.literal_eval(
                restaurant['restaurant_image_url'])
            restaurant['offer_options'] = ast.literal_eval(
                restaurant['offer_options'])
            restaurant['payment_methods'] = ast.literal_eval(
                restaurant['payment_methods'])
            return JsonResponse(restaurant)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def put(self, request):
        """Edit a restaurant profile and save it as a draft in the database"""
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data,
                     schema=restaurant_edit_draft_schema)
            body = request.data
            invalid = PendingRestaurant.field_validate_draft(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({'message': 'restaurant with owner user id '+user_id+' does not exist'}, status=404)
            if 'email' in body and body['email'] != restaurant.email:
                return JsonResponse({'message': "You're not allowed to modify your restaurant's email address"}, status=400)
            body["status"] = Status.In_Progress.value
            body["modified_time"] = timezone.now()
            edit_model(restaurant, body, restaurant_editable)
            if address_changed(body):
                address = restaurant.address + ', ' + restaurant.postalCode + ', Ontario'
                update_model_geo(restaurant, address)
            restaurant = model_to_json(save_and_clean(restaurant))
            restaurant['restaurant_image_url'] = ast.literal_eval(
                restaurant['restaurant_image_url'])
            restaurant['offer_options'] = ast.literal_eval(
                restaurant['offer_options'])
            restaurant['payment_methods'] = ast.literal_eval(
                restaurant['payment_methods'])
            return JsonResponse(restaurant)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

# insert_restaurant_for_approval_page

class RestaurantForApprovalView(APIView):
    """ inser restaurant for approval view """
    #permission_classes = (AllowAny,)

    def put(self, request):
        """ Insert or update a restaurant record for admin approval """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data,
                     schema=restaurant_insert_for_approval_schema)
            body = request.data
            invalid = PendingRestaurant.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)

            rest_filter = PendingRestaurant.objects.filter(owner_user_id=user_id)
            if not rest_filter.exists():
                body['status'] = Status.Pending.value
                restaurant = PendingRestaurant.insert(body)
            else:
                restaurant = rest_filter.first()
                body['status'] = Status.Pending.value
                body["modified_time"] = timezone.now()
                edit_model(restaurant, body, restaurant_editable)
                if address_changed(body):
                    address = restaurant.address + ', ' + restaurant.postalCode + ', Ontario'
                    update_model_geo(restaurant, address)
                restaurant = save_and_clean(restaurant)
            return JsonResponse(model_to_json(restaurant))
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': e.message}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)


def address_changed(body):
    """
    return if address has changed
    @param body: edited fields
    @return: boolean
    """
    return 'address' in body


def category_is_changed(body):
    """
    check whether category was edited
    @param body: request body for editing
    @return: boolean
    """
    return 'category' in body


def new_category(category, restaurant):
    """
    check if category is new to restaurant
    @param category: restaurant category
    @param restaurant: referenced restaurant
    @return: boolean
    """
    return category not in restaurant.categories


def should_add_category(body, category, restaurant):
    """
    check if should add category
    @param body:
    @param category:
    @param restaurant:
    @return:
    """
    return new_category(category, restaurant)


def add_cateogory(category, restaurant):
    """
    add new category to restaurant
    @param category:
    @param restaurant:
    @return:
    """
    restaurant.categories.append(category)
    restaurant.save(update_fields=['categories'])


class AnalyticsAccessTokenView(APIView):
    """ analytics access token view """

    def get(self, request):
        """ Get OAuth2 access token for Google Analytics API to make call """
        return JsonResponse({'token': get_access_token()})

class AnalyticsDataView(APIView):
    """ analytics data view """

    def get(self, request, rest_id):
        """ Retrieves analytics data for a restaurant page given restaurant id """
        #restaurant_id = request.GET.get('restaurant_id')
        traffic = get_analytics_data(rest_id)
        return JsonResponse(traffic)


class PostView(APIView):
    """ Restaurant posts view """
    #permission_classes = (AllowAny,)

    def post(self, request):
        """ Insert a new post for a restaurant """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']

            validate(instance=request.data, schema=post_schema)
            body = request.data
            body['owner_user_id'] = user_id
            invalid = RestaurantPost.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)

            post = RestaurantPost.insert(body)
            return JsonResponse(model_to_json(post))
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'error': e.message}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def get(self, request):
        """ Get all posts for a restaurant """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']
            posts = list(RestaurantPost.objects.filter(owner_user_id=user_id))
            response = {"Posts": []}
            for post in posts:
                time_stamp = {"Timestamp": post.timestamp.strftime("%b %d, %Y %H:%M")}
                response["Posts"].append(model_to_json(post, time_stamp))
            return JsonResponse(response)
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def delete(self, request, post_id):
        """ Deletes a single restaurant post """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)

            post_filter = RestaurantPost.objects.filter(_id=post_id)
            post = post_filter.first()
            if not post:
                return JsonResponse({"message": "no post found with this id: "+post_id}, status=404)

            post_deleted = model_to_json(post)
            post_filter.delete()
            return JsonResponse({"Post delete": post_deleted})
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)


class RestaurantMediaView(APIView):
    """ Restaurant media (image/video) view """
    #permission_classes = (AllowAny,)

    def put(self, request):
        """ For inserting or updating restaurant media """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({"error": "Could not find restaurant owned by this user"}, status=400)

            form = RestaurantMediaForm(request.data, request.FILES)
            if not form.is_valid():
                return JsonResponse({"error": form.errors}, status=400)

            restaurant = PendingRestaurant.upload_media(restaurant, request.data, request.FILES)
            return JsonResponse(model_to_json(restaurant))
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)

    def delete(self, request):
        """ For removing image(s) from the restaurant_image_url field and Google Cloud bucket """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']
            form_data = request.data
            restaurant = PendingRestaurant.objects.filter(owner_user_id=user_id).first()
            if not restaurant:
                return JsonResponse({"error": "Could not find restaurant owned by this user"}, status=400)

            form = RestaurantImageDeleteForm(form_data, request.FILES)
            if not form.is_valid():
                return JsonResponse({"error": form.errors}, status=400)

            restaurant = PendingRestaurant.delete_media(restaurant, form_data)
            return JsonResponse(model_to_json(restaurant))
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)


class DishMediaView(APIView):
    """ Dish media (image) view """
    #permission_classes = (AllowAny,)

    def put(self, request, dish_id):
        """ For inserting or updating restaurant media """
        try:
            user = get_user(request)
            if not user:
                return JsonResponse({'message': 'fail to obtain user', 'code': 'fail_obtain_user'}, status=405)
            user_id = user['user_id']
            dish = PendingFood.objects.filter(_id=dish_id).first()
            if not dish:
                return JsonResponse({"error": "Could not find the dish with id: "+dish_id}, status=400)

            form = FoodMediaForm(request.data, request.FILES)
            if not form.is_valid():
                return JsonResponse({"error": form.errors}, status=400)

            dish = PendingFood.upload_media(dish, request.data, request.FILES)
            return JsonResponse(model_to_json(dish))
        except Exception as e:
            message = 'something went wrong'
            if hasattr(e, 'message'):
                message = e.message
            return JsonResponse({'error': message}, status=500)