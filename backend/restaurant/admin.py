from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.http import HttpResponse, HttpResponseRedirect

from utils.geo_controller import geocode
from utils.model_util import save_and_clean, model_to_json, edit_model
from utils.admin import InputFilter, OwnerNameFilter, NameFilter, PriceMaxFilter, PriceMinFilter

from restaurant.enum import Status
from restaurant.forms import RestaurantAdminForm
from restaurant.models import PendingRestaurant, PendingFood, Restaurant, Food, UserFavRestrs, RestaurantPost
from restaurant.utils import send_approval_email, send_reject_email, send_unpublish_email

from django.contrib import messages
from utils.geo_controller import geocode
from utils.cloud_storage import delete
import ast
# from decimal import Decimal
#from django.contrib.admin.actions import delete_selected


def reject_restr(model_admin, request, queryset):
    """
    Reject a Restaurant and unpublish it if the current one on
    live site is the same as the submission.
    Sends a notification email to the restaurant email for
    each successful rejection.
    """
    count = 0
    total = 0
    restaurant_name = ""
    restaurant_id = None
    for r in queryset:
        total += 1
        res_dict = model_to_json(r)
        res_status = res_dict['status']
        # note that if the submission is already rejected then it will not be
        # on the live site
        if res_status != Status.Rejected.value:
            count += 1
            restaurant_name = res_dict.get('name', "")
            restaurant_id = res_dict["_id"]
            owner_prefer_names = res_dict.get('owner_preferred_name', "")
            email = res_dict.get('email', "")
            send_reject_email(
                owner_prefer_names,
                email,
                restaurant_name,
                'restaurant')
            # restaurant that is being displayed on the live site
            restaurant = Restaurant.objects.get(_id=restaurant_id)
            if restaurant:
                restaurant.delete()
    # change status to reject
    queryset.update(status=Status.Rejected.value)
    if count > 1:
        messages.success(
            request,
            "Successfully rejected " +
            str(count) +
            " restaurant profiles.")
    elif count == 1:
        link = reverse(
            "admin:restaurant_pendingrestaurant_change",
            args=[restaurant_id])
        msg = format_html(
            "Successfully rejected restaurant profile for <a href='{}' target='_blank' rel='noopener'>{}</a>",
            link,
            restaurant_name)
        messages.success(request, msg)
    else:
        if total > 1:
            msg = "The selected restaurant profiles have been rejected already."
        else:
            msg = "The selected restaurant profile has been rejected already."
        messages.error(request, msg)


reject_restr.short_description = "Reject a restaurant submission (and unpublish from live site if the submission was in approved state)"


def unpublish_restr(model_admin, request, queryset):
    """
    Unpublish a live Restaurant Profile and updates the
    status of pendingRestaurant accordingly.
    Sends a notification email to the restaurant email for
    each successful unpublish action.
    """
    count = 0
    restaurant_name = ""
    for r in queryset:
        count += 1
        res_dict = model_to_json(r)

        owner_prefer_names = res_dict.get('owner_preferred_name', "")
        restaurant_name = res_dict.get('name', "")
        email = res_dict.get('email', "")
        send_unpublish_email(
            owner_prefer_names,
            email,
            restaurant_name,
            'restaurant')
        restaurant_id = res_dict["_id"]
        pendingRestaurant = PendingRestaurant.objects.get(_id=restaurant_id)
        # change approved pendingRestaurant to rejected as the profile is being
        # unpublished
        if pendingRestaurant.status == Status.Approved.value:
            pendingRestaurant.status = Status.Rejected.value
            pendingRestaurant.save()
        # Remove all user-restaurant favourite relation records
        # that contains the unpublished restaurant
        UserFavRestrs.objects.filter(restaurant=restaurant_id).delete()
    queryset.delete()
    if count > 1:
        messages.success(
            request,
            "Successfully unpublished " +
            str(count) +
            " restaurant profiles.")
    elif count == 1:
        msg = "Successfully unpublished restaurant profile for " + restaurant_name
        messages.success(request, msg)


unpublish_restr.short_description = "Unpublish a restaurant (remove it from live site and change the status of its corresponding submission)"


def approve_restr(model_admin, request, queryset):
    """
    Approve of PendingRestaurant record and insert it into Restaurant collection,
    or updates the existing record in Restaurant collection that corresponds to
    this PendingRestaurant record.
    Sends a notification email to the restaurant email
    for each successful approval.
    """
    count = 0
    total = 0
    restaurant_name = ""
    restaurant_id = None
    for r in queryset:
        total += 1
        print(r._id)
        restaurant = Restaurant(**model_to_json(r))
        old_restaurant = Restaurant.objects.filter(_id=r._id).first()

        if r.status == Status.Pending.value:
            count += 1

            # If there's already an approved restaurant record in Restaurant collection
            # check if the restaurant's media (image or video) is oudated, by comparing the url
            # to the url in the PendingRestaurant's media fields. If they don't match
            # delete the approved restaurant record's media file from google cloud bucket
            if old_restaurant:
                if old_restaurant.logo_url != r.logo_url:
                    delete(old_restaurant.logo_url)
                if old_restaurant.cover_photo_url != r.cover_photo_url:
                    delete(old_restaurant.cover_photo_url)
                if (old_restaurant.restaurant_video_url != r.restaurant_video_url
                        and 'youtube' not in old_restaurant.restaurant_video_url):
                    delete(old_restaurant.restaurant_video_url)
            edit_model(
                restaurant, {
                    "status": Status.Approved.value, "approved_once": True}, [
                    "status", "approved_once"])
            save_and_clean(restaurant)
            owner_prefer_names = r.owner_preferred_name
            restaurant_name = r.name
            email = r.email
            restaurant_id = r._id
            send_approval_email(
                owner_prefer_names,
                email,
                restaurant_name,
                'restaurant')
        else:
            messages.error(
                request, "You can only approve of 'Pending' restaurants")
    queryset.update(status=Status.Approved.value, approved_once=True)
    if count > 1:
        messages.success(
            request,
            "Successfully approved " +
            str(count) +
            " restaurant profiles.")
    elif count == 1:
        link = reverse(
            "admin:restaurant_pendingrestaurant_change",
            args=[restaurant_id])
        msg = format_html(
            "Successfully approved restaurant profile for <a href='{}' target='_blank' rel='noopener'>{}</a>",
            link,
            restaurant_name)
        messages.success(request, msg)
    else:
        if total > 1:
            msg = "The selected restaurant profiles have been approved already."
        else:
            msg = "The selected restaurant profile has been approved already."
        messages.error(request, msg)


approve_restr.short_description = "Approve of restaurant info to be displayed on website"


def reject_food(model_admin, request, queryset):
    """
    Reject a Food and unpublish it if the current one on
    live site is the same as the submission.
    Sends a notification email to the restaurant email for
    each successful rejection.
    """
    count = 0
    total = 0
    for f in queryset:
        total += 1
        restaurant = PendingRestaurant.objects.filter(_id=f.restaurant_id)
        # note that if the submission is already rejected then it will not be
        # on the live site
        if f.status != Status.Rejected.value:
            count += 1
            restr = restaurant.first()
            owner_prefer_names = restr.owner_preferred_name
            food_name = f.name
            email = restr.email
            send_reject_email(owner_prefer_names, email, food_name, 'food')
            # restaurant that is being displayed on the live site
            food = Food.objects.filter(_id=f._id)
            if food.exists():
                food.delete()
    # change status to reject
    queryset.update(status=Status.Rejected.value)
    if count > 1:
        messages.success(
            request,
            "Successfully rejected " +
            str(count) +
            " food profiles.")
    elif count == 1:
        link = reverse("admin:restaurant_pendingfood_change", args=[f._id])
        msg = format_html(
            "Successfully rejected food profile for <a href='{}' target='_blank' rel='noopener'>{}</a>",
            link,
            f.name)
        messages.success(request, msg)
    else:
        if total > 1:
            msg = "The selected food profiles have been rejected already."
        else:
            msg = "The selected food profile has been rejected already."
        messages.error(request, msg)


reject_food.short_description = "Reject a food submission (and unpublish from live site if the submission was in approved state)"


def unpublish_food(model_admin, request, queryset):
    """
    Unpublish a live Restaurant Dish Profile and updates
    the status of pendingDish accordingly.
    Sends a notification email to the restaurant email for
    each successful unpublish action.
    """
    count = 0
    for f in queryset:
        count += 1
        pendingFood = PendingFood.objects.filter(_id=f._id).first()
        restaurant = PendingRestaurant.objects.filter(_id=f.restaurant_id)
        if pendingFood.status == Status.Approved.value:
            restr = restaurant.first()
            owner_prefer_names = restr.owner_preferred_name
            food_name = f.name
            email = restr.email
            send_unpublish_email(owner_prefer_names, email, food_name, 'food')
            pendingFood.status = Status.Rejected.value
            save_and_clean(pendingFood)
    queryset.delete()
    if count > 1:
        messages.success(
            request,
            "Successfully unpublished " +
            str(count) +
            " food profiles.")
    elif count == 1:
        msg = "Successfully unpublished food profile for " + f.name
        messages.success(request, msg)


unpublish_food.short_description = "Unpublish a food (remove it from live site and change the status of its corresponding submission)"


def approve_food(model_admin, request, queryset):
    """ Approve of PendingFood record and insert it into Food collection,
    or updates the existing record in Food collection that corresponds to
    this PendingFood record.
    Sends a notification email to the restaurant email
    for each successful approval.
    """
    count = 0
    total = 0
    for f in queryset:
        total += 1
        food = Food(**model_to_json(f))
        old_food = Food.objects.filter(_id=f._id).first()
        restaurant = PendingRestaurant.objects.filter(_id=f.restaurant_id)
        if restaurant.exists() and f.status != 'Approved':
            count += 1
            restr = restaurant.first()
            owner_prefer_names = restr.owner_preferred_name
            food_name = f.name
            email = restr.email
            send_approval_email(owner_prefer_names, email, food_name, 'food')

            # If there's already an approved food record in Food collection
            # check if the food's picture is oudated, by comparing the url
            # to the url in the PendingFood's picture field. If they don't match
            # delete the approved food record's picture from google cloud bucket
            if old_food:
                if old_food.picture != f.picture:
                    delete(old_food.picture)
            food.status = Status.Approved.value
            save_and_clean(food)
    queryset.update(status=Status.Approved.value)
    if count > 1:
        messages.success(
            request,
            "Successfully approved " +
            str(count) +
            " food profiles.")
    elif count == 1:
        link = reverse("admin:restaurant_pendingfood_change", args=[f._id])
        msg = format_html(
            "Successfully approved restaurant profile for <a href='{}' target='_blank' rel='noopener'>{}</a>",
            link,
            f.name)
        messages.success(request, msg)
    else:
        if total > 1:
            msg = "The selected food profiles have been approved already."
        else:
            msg = "The selected food profile has been approved already."
        messages.error(request, msg)


approve_food.short_description = "Approve of restaurant dish to be displayed on website"


class PendingRestrAdmin(admin.ModelAdmin):
    """ Admin Model for PendingRestaurant """

    list_filter = ('status', NameFilter, OwnerNameFilter)
    list_display = (
        'name',
        'status',
        'owner_first_name',
        'owner_last_name',
        'owner_preferred_name',
        'cuisines',
        'address',
        'categories',
        'coverPhotoUrl',
        'logoUrl',
        'modified_time')
    actions = (approve_restr, reject_restr)
    readonly_fields = ('status', 'GEO_location',)

    def save_model(self, request, obj, form, change):
        """
        Overridden save method so GEO_location field will be updated
        when address is updated
        """
        restaurant = obj
        restaurant.GEO_location = geocode(restaurant.address)
        restaurant.clean()
        restaurant.clean_fields()
        restaurant.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        # unpublish will take care the deletion (because it will update the
        # corresponding Restaurant)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def categories(self, obj):
        return ', '.join(obj.categories)

    def coverPhotoUrl(self, obj):
        return format_html(
            "<a href='{url}'>{url}</a>",
            url=obj.cover_photo_url)

    def logoUrl(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.logo_url)

    coverPhotoUrl.short_description = "cover_photo_url"
    logoUrl.short_description = "logo_url"

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            approve_restr(
                self,
                request,
                PendingRestaurant.objects.filter(
                    _id=obj._id))
            return HttpResponseRedirect(".")

        if "_reject" in request.POST:
            reject_restr(
                self,
                request,
                PendingRestaurant.objects.filter(
                    _id=obj._id))
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)


class RestaurantFilter(admin.SimpleListFilter):
    """ Filter by Restaurant for PendingFood Admin Model """
    title = 'restaurant'
    parameter_name = 'restaurant_id'

    def lookups(self, request, model_admin):
        restaurants = []
        qs = set([f.restaurant_id for f in model_admin.model.objects.all()])
        for r_id in qs:
            restaurant_name = PendingRestaurant.get(r_id).name
            restaurants.append((r_id, restaurant_name))
        return restaurants

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        return queryset.filter(restaurant_id__exact=value)


class PendingFoodAdmin(admin.ModelAdmin):
    """ Admin Model for PendingFood """
    list_filter = ('status', NameFilter, RestaurantFilter,)
    list_display = (
        'name',
        'restaurant',
        'description',
        'pictureUrl',
        'price',
        'specials',
        'category',
        'status',
        'link_to_restaurant',
    )
    readonly_fields = ('restaurant_id', 'status')
    actions = (approve_food, reject_food,)

    def save_model(self, request, obj, form, change):
        """
        Overridden save method so corresponding restaurant object
        can update its categories field; also checks to make sure
        signature dish and popular dish limits are obeyed
        """
        food = obj
        restaurant = PendingRestaurant.objects.filter(
            _id=food.restaurant_id).first()
        if (food.category == 'Signature Dish' and PendingFood.objects.filter(
                restaurant_id=food.restaurant_id, category='Signature Dish').count() == 1):
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'A restaurant can only have 1 signature dish.')
        elif (food.category == 'Popular Dish' and
              PendingFood.objects.filter(restaurant_id=food.restaurant_id, category='Popular Dish').count() == 6):
            if food._id not in list(
                PendingFood.objects.filter(
                    restaurant_id=food.restaurant_id,
                    category='Popular Dish').values_list(
                    '_id',
                    flat=True)):
                messages.set_level(request, messages.ERROR)
                messages.error(
                    request, 'A restaurant can only have up to 6 popular dishes.')
        else:
            food.clean()
            food.clean_fields()
            food.save()
            restaurant.categories = PendingFood.get_all_categories(
                food.restaurant_id)
            restaurant.clean()
            restaurant.clean_fields()
            restaurant.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def pictureUrl(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.picture)

    def restaurant(self, obj):
        restaurant_name = PendingRestaurant.get(obj.restaurant_id).name
        return restaurant_name

    def link_to_restaurant(self, obj):
        # link to edit restaurant associated with restaurant id
        # first argument of reverse takes a string (all lowercase) in the form of "admin:appname_modelname_change" for edit
        # target='_blank' has no effect, open new tab doesn't work at the
        # moment, ignore it for now
        try:
            if not obj.restaurant_id:
                return ""
            link = reverse(
                "admin:restaurant_pendingrestaurant_change", args=[
                    obj.restaurant_id])
            return format_html(
                "<a href='{}' target='_blank' rel='noopener'>{}</a>",
                link,
                obj.restaurant_id)
        except NoReverseMatch as e:
            return str(obj.restaurant_id)
        except Exception as e:
            return str(obj.restaurant_id)

    pictureUrl.short_description = "picture"
    link_to_restaurant.short_description = 'restaurant_id'

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            approve_restr(
                self,
                request,
                PendingFood.objects.filter(
                    _id=obj._id))
            return HttpResponseRedirect(".")

        if "_reject" in request.POST:
            reject_restr(
                self,
                request,
                PendingFood.objects.filter(
                    _id=obj._id))
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)


class RestrAdmin(admin.ModelAdmin):
    """ Admin Model for Restaurant """
    list_filter = ('status', NameFilter, OwnerNameFilter)
    list_display = (
        'name',
        'owner_first_name',
        'owner_last_name',
        'owner_preferred_name',
        'cuisines',
        'address',
        'categories',
        'coverPhotoUrl',
        'logoUrl')
    actions = (unpublish_restr,)
    readonly_fields = ('status', 'GEO_location',)
    change_list_template = 'restaurant/change_list_graph.html'
    change_form_template = 'restaurant/change_form_graph.html'

    def save_model(self, request, obj, form, change):
        """
        Overridden save method so GEO_location field will be updated
        when address is updated
        """
        restaurant = obj
        restaurant.GEO_location = geocode(restaurant.address)
        restaurant.clean()
        restaurant.clean_fields()
        restaurant.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        delete_action = 'delete_selected'
        # unpublish will take care the deletion (because it will update the
        # corresponding pendingRestaurant)
        if delete_action in actions:
            del actions[delete_action]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        form = RestaurantAdminForm

    def get_form(self, request, obj=None, **kwargs):

        kwargs['form'] = RestaurantAdminForm
        return super().get_form(request, obj, **kwargs)

    def categories(self, obj):
        return ', '.join(obj.categories)

    def coverPhotoUrl(self, obj):
        return format_html(
            "<a href='{url}'>{url}</a>",
            url=obj.cover_photo_url)

    def logoUrl(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.logo_url)

    coverPhotoUrl.short_description = "cover_photo_url"
    logoUrl.short_description = "logo_url"

    def response_change(self, request, obj):
        if "_unpublish" in request.POST:
            unpublish_restr(
                self,
                request,
                Restaurant.objects.filter(
                    _id=obj._id))
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)


class FoodAdmin(admin.ModelAdmin):
    """ Admin Model for Food """
    list_filter = ('status', NameFilter, RestaurantFilter,)
    list_display = (
        'name',
        'restaurant',
        'description',
        'pictureUrl',
        'price',
        'specials',
        'category',
        'status',
        'link_to_restaurant',
    )
    readonly_fields = ('restaurant_id', 'status')
    actions = (unpublish_food,)

    def response_change(self, request, obj):
        if "_unpublish" in request.POST:
            unpublish_food(self, request, Food.objects.filter(_id=obj._id))
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Overridden save method so corresponding restaurant object
        can update its categories field; also checks to make sure
        signature dish and popular dish limits are obeyed
        """
        food = obj
        restaurant = Restaurant.objects.filter(_id=food.restaurant_id).first()
        if (food.category == 'Signature Dish' and Food.objects.filter(
                restaurant_id=food.restaurant_id, category='Signature Dish').count() == 1):
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'A restaurant can only have 1 signature dish.')
        elif (food.category == 'Popular Dish' and
              Food.objects.filter(restaurant_id=food.restaurant_id, category='Popular Dish').count() == 6):
            if food._id not in list(
                Food.objects.filter(
                    restaurant_id=food.restaurant_id,
                    category='Popular Dish').values_list(
                    '_id',
                    flat=True)):
                messages.set_level(request, messages.ERROR)
                messages.error(
                    request, 'A restaurant can only have up to 6 popular dishes.')
        else:
            food.clean()
            food.clean_fields()
            food.save()
            restaurant.categories = Food.get_all_categories(food.restaurant_id)
            restaurant.clean()
            restaurant.clean_fields()
            restaurant.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def pictureUrl(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.picture)

    def restaurant(self, obj):
        restaurant_name = PendingRestaurant.get(obj.restaurant_id).name
        return restaurant_name

    def link_to_restaurant(self, obj):
        # link to edit restaurant associated with restaurant id
        # first argument of reverse takes a string (all lowercase) in the form of "admin:appname_modelname_change" for edit
        # target='_blank' has no effect, open new tab doesn't work at the
        # moment, ignore it for now
        try:
            if not obj.restaurant_id:
                return ""
            link = reverse(
                "admin:restaurant_pendingrestaurant_change", args=[
                    obj.restaurant_id])
            return format_html(
                "<a href='{}' target='_blank' rel='noopener'>{}</a>",
                link,
                obj.restaurant_id)
        except NoReverseMatch as e:
            return str(obj.restaurant_id)
        except Exception as e:
            return str(obj.restaurant_id)

    pictureUrl.short_description = "picture"
    link_to_restaurant.short_description = 'restaurant_id'

    def response_change(self, request, obj):
        if "_unpublish" in request.POST:
            unpublish_restr(self, request, Food.objects.filter(_id=obj._id))
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)


class RestPostAdmin(admin.ModelAdmin):
    list_filter = (RestaurantFilter, 'timestamp',)
    list_display = (
        'restaurant_name',
        'link_to_restaurant',
        'owner_user_id',
        'timestamp',
    )

    readonly_fields = ('restaurant_id',)

    def restaurant_name(self, obj):
        if not obj.restaurant_id:
            return ""
        return PendingRestaurant.objects.filter(
            _id=obj.restaurant_id).first().name

    def link_to_post_edit(self, obj):
        link = reverse(
            "admin:restaurant_restaurantpost_change",
            args=[
                obj._id])
        return format_html(
            "<a href='{}' target='_blank' rel='noopener'>{}</a>",
            link,
            obj.restaurant_id)

    def link_to_restaurant(self, obj):
        # link to edit restaurant associated with restaurant id
        # first argument of reverse takes a string (all lowercase) in the form of "admin:appname_modelname_change" for edit
        # target='_blank' has no effect, open new tab doesn't work at the
        # moment, ignore it for now
        try:
            if not obj.restaurant_id:
                return ""
            link = reverse(
                "admin:restaurant_pendingrestaurant_change", args=[
                    obj.restaurant_id])
            return format_html(
                "<a href='{}' target='_blank' rel='noopener'>{}</a>",
                link,
                obj.restaurant_id)
        except NoReverseMatch as e:
            return str(obj.restaurant_id)
        except Exception as e:
            return str(obj.restaurant_id)


admin.site.register(PendingRestaurant, PendingRestrAdmin)
admin.site.register(PendingFood, PendingFoodAdmin)
admin.site.register(Restaurant, RestrAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(RestaurantPost, RestPostAdmin)
