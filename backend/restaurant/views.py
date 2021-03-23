from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from restaurant.enum import Status
from restaurant.models import (
    Food,
    Restaurant,
    PendingRestaurant,
    PendingFood,
    UserFavRestrs
)

from utils.model_util import model_to_json, save_and_clean, edit_model, update_model_geo, models_to_json

from bson import ObjectId
import ast

# jsonschema validation schemes

food_schema = {
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "restaurant_id": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": ["string", "number"]},
        "tags": {"type": "array",
                 "items": {"type": "string"}
                 },
        "specials": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["name", "restaurant_id", "description", "price", "specials", "category"],
    "additionalProperties": False
}

food_edit_schema = {
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "restaurant_id": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": ["string", "number"]},
        "tags": {"type": "array",
                 "items": {"type": "string"}
                 },
        "specials": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["_id"],
    "additionalProperties": False
}


restaurant_insert_for_approval_schema = {
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
    "required": ["name", "years", "address", "postalCode", "phone", "email", "pricepoint", "offer_options",
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
    "required": ["name", "address", "postalCode", "email", "owner_first_name", "owner_last_name"],
    "additionalProperties": False
}

restaurant_edit_draft_schema = {
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
    "required": ["restaurant_id"],
    "additionalProperties": False
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

    def get(self, request, rest_id):
        """Retrieve all dishes from the database"""
        foods = Food.objects.all()
        response = {'Dishes': models_to_json(foods)}
        return JsonResponse(response)


class DishRestaurantView(APIView):
    """ dish restaurant view """

    def get(self, request, rest_id):
        """Retrieve all dishes from a restaurant"""
        # rest_id = request.GET.get('restaurant_id')
        dishes = Food.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)

    def post(self, request, rest_id):
        """ Deletes dish from database """
        try:
            body = json.loads(request.body)
            food = PendingFood.objects.get(
                name=body["food_name"], restaurant_id=rest_id)
            food.delete()
            Food.objects.filter(
                name=body['food_name'], restaurant_id=rest_id).delete()
            restaurant = PendingRestaurant.objects.get(_id=rest_id)

            restaurant_categories = PendingFood.get_all_categories(
                restaurant._id)
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
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


class PendingDishView(APIView):
    """ pending dish view """

    def get(self, request, rest_id):
        """Retrieve all dishes from a restaurant"""
        # rest_id = request.GET.get('restaurant_id')
        dishes = PendingFood.get_by_restaurant(rest_id)
        response = {'Dishes': models_to_json(dishes)}
        return JsonResponse(response)

    def post(self, request, rest_id):
        """ Insert dish into database """
        try:
            validate(instance=json.loads(request.body), schema=food_schema)
            body = json.loads(request.body)
            invalid = PendingFood.field_validate(body)
            if invalid:
                return JsonResponse(invalid)

            if PendingFood.objects.filter(restaurant_id=rest_id, category='Popular Dish').count() == 6 and body['category'] == 'Popular Dish':
                return JsonResponse({'message': 'You can only have up to a maximum of 6 popular dishes.'}, status=400)
            if PendingFood.objects.filter(restaurant_id=rest_id, category='Signature Dish').count() == 1 and body['category'] == 'Signature Dish':
                return JsonResponse({'message': 'You can only have 1 signature dish.'}, status=400)

            food = PendingFood.add_dish(body)
            return JsonResponse(model_to_json(food))
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            body = json.loads(request.body)
            PendingFood.objects.filter(
                restaurant_id=body['restaurant_id'], name=body['name']).delete()
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

    def put(self, request, rest_id):
        """ Update Dish data """
        try:
            validate(instance=json.loads(request.body),
                     schema=food_edit_schema)
            body = json.loads(request.body)
            invalid = PendingFood.field_validate(body)
            if invalid is not None:
                return JsonResponse(invalid)

            dish = PendingFood.objects.get(_id=rest_id)
            restaurant = PendingRestaurant.objects.get(_id=dish.restaurant_id)
            if should_add_category(body, dish.category, restaurant):
                add_cateogory(dish.category, restaurant)

            restaurant_editable = ["status"]
            restaurant_editable_values = {'status': Status.Pending.value}

            if 'category' in body and PendingFood.objects.filter(restaurant_id=restaurant._id, category=body['category']).exists():
                if (body['category'] == 'Popular Dish' and PendingFood.objects.filter(restaurant_id=restaurant._id, category='Popular Dish').count() == 6):
                    if ObjectId(body['_id']) not in list(PendingFood.objects.filter(restaurant_id=restaurant._id, category='Popular Dish').values_list('_id', flat=True)):
                        return JsonResponse({'message': 'You can only have up to a maximum of 6 popular dishes.'}, status=400)
                if (body['category'] == 'Signature Dish' and PendingFood.objects.filter(restaurant_id=restaurant._id, category='Signature Dish').count() == 1):
                    if body['_id'] != str(PendingFood.objects.filter(restaurant_id=restaurant._id, category='Signature Dish').first()._id):
                        return JsonResponse({'message': 'You can only have 1 signature dish.'}, status=400)
                restaurant_editable.append("categories")

            body["status"] = Status.Pending.value
            edit_model(dish, body, dish_editable)
            updated_fields = [field for field in body.keys()]
            updated_fields.remove('_id')
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
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


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

    def post(self, request, user_id):
        """ Add a new user-restaurant-favourite relation """
        try:
            body = json.loads(request.body)
            body['user_id'] = user_id
            invalid = UserFavRestrs.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            response = UserFavRestrs.insert(body)
            return JsonResponse(response)
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

    def get(self, request, user_id):
        """ Get all restaurants favourited by a user """
        try:
            # user_id = request.GET.get('user_id')
            response = UserFavRestrs.getUserFavourites(user_id)
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        except Exception as e:
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

# get_user_favs_restr_page

class UserFavRestaurantView(APIView):
    """ user fav restaurants view """

    def get(self, request, rest_id):
        """ Get all users who favourited the requested restaurant """
        try:
            # _id = request.GET.get('restaurant_id')
            response = UserFavRestrs.getRestrFavouriteds(rest_id)
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=404)
        except Exception as e:
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

# remove_fav_page

class FavRelationView(APIView):
    """ remove fav relation view """

    def delete(self, request, user_id, rest_id):
        """ Remove a new user-restaurant-favourite relation """
        try:

            # body = json.loads(request.body)
            body = {'user_id': user_id, 'restaurant_id': rest_id}
            invalid = UserFavRestrs.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            response = UserFavRestrs.remove_fav(body)
            return JsonResponse(response, safe=False)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=500)
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'message': e.message}, status=500)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=500)
        except Exception as e:
            UserFavRestrs.objects.create(
                user=user_id, restaurant=rest_id).save()
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


class RestaurantView(APIView):
    """ get restaurant view dish view """

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

    def get(self, request, rest_id):
        """Retrieve restaurant from pending collection by id"""
        try:
            # _id = request.GET.get('_id')
            _id = rest_id
            if _id is None:
                return JsonResponse({'message': '_id parameter is required and cannot be None'}, status=400)

            restaurant = PendingRestaurant.get(_id)
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
                return JsonResponse({'message': 'No pending restaurant found with this id: '+_id}, status=404)
        except Exception:
            return JsonResponse({'message': 'Something went wrong'}, status=500)

# get_all_restaurants_page

class AllRestaurantList(APIView):
    """ all restaurants list """

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

    def post(self, request):
        """Insert new restaurant as a draft into database"""
        try:
            validate(instance=json.loads(request.body),
                     schema=restaurant_insert_draft_schema)
            body = json.loads(request.body)
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
            body = json.loads(request.body)
            PendingRestaurant.objects.filter(email=body['email']).delete()
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

    def put(self, request):
        """Edit a restaurant profile and save it as a draft in the database"""
        try:
            validate(instance=json.loads(request.body),
                     schema=restaurant_edit_draft_schema)
            body = json.loads(request.body)
            invalid = PendingRestaurant.field_validate_draft(body)
            if invalid:
                return JsonResponse(invalid, status=400)
            restaurant = PendingRestaurant.get(body["restaurant_id"])
            if not restaurant:
                return JsonResponse({'message': 'restaurant with id '+body['restaurant_id']+' does not exist'}, status=404)
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
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)

# insert_restaurant_for_approval_page

class RestaurantForApprovalView(APIView):
    """ inser restaurant for approval view """

    def post(self, request):
        """Insert or update a restaurant record for admin approval"""
        try:
            validate(instance=json.loads(request.body),
                     schema=restaurant_insert_for_approval_schema)
            body = json.loads(request.body)
            invalid = PendingRestaurant.field_validate(body)
            if invalid:
                return JsonResponse(invalid, status=400)

            restaurant = {}
            restaurant_filter = PendingRestaurant.objects.filter(
                email=body['email'])
            if not restaurant_filter.exists():
                restaurant = model_to_json(PendingRestaurant.insert(body))
                restaurant['status'] = Status.Pending.value
                restaurant['restaurant_image_url'] = ast.literal_eval(
                    restaurant['restaurant_image_url'])
                restaurant['offer_options'] = ast.literal_eval(
                    restaurant['offer_options'])
                restaurant['payment_methods'] = ast.literal_eval(
                    restaurant['payment_methods'])
            else:
                restaurant = restaurant_filter.first()
                body['status'] = Status.Pending.value
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
            body = json.loads(request.body)
            PendingRestaurant.objects.filter(email=body['email']).delete()
            message = 'something went wrong'
            try:
                message = getattr(e, 'message', str(e))
            except Exception as e:
                message = getattr(e, 'message', 'something went wrong')
            finally:
                return JsonResponse({'message': message}, status=500)


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
