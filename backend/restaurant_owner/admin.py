from django.contrib import admin
from django.urls.exceptions import NoReverseMatch
from django.urls import reverse
from django.utils.html import format_html

from restaurant_owner.models import RestaurantOwner
from restaurant.models import PendingRestaurant
from sduser.models import SDUser

from utils.common import isObjectId
from utils.filters import UserIDFilter, RestaurantIDFilter


class RestaurantOwnerAdmin(admin.ModelAdmin):
    """ Admin Model for RestaurantOwner """
    list_filter = (UserIDFilter, RestaurantIDFilter, 'consent_status',)
    list_display = ('user_id', 'link_to_user', 'restaurant_name', 'link_to_restaurant',
                    'last_updated', 'consent_status', 'subscribed_at', 'expired_at', 'unsubscribed_at',)
    list_display_links = ('user_id',)

    def link_to_user(self, obj):
        try:
            user_id = obj.user_id
            user = SDUser.objects.get(id=user_id)
            link = reverse("admin:sduser_sduser_change", args=[user_id])
            return format_html("<a href='{}' target='_blank' rel='noopener'>{}</a>", link, user.username)
        except NoReverseMatch as e:
            raise e
            return str(user_id)
        except Exception as e:
            raise e
            return str(user_id)

    link_to_user.short_description = "username (link to sduser)"

    def restaurant_name(self, obj):
        oid = obj.restaurant_id
        if isObjectId(oid):
            try:
                restaurant = PendingRestaurant.get(obj.restaurant_id)
                if restaurant:
                    restaurant_name = restaurant.name
                else:
                    restaurant_name = "None"
            except Exception:
                return ""
        else:
            restaurant_name = ""
        return restaurant_name

    def link_to_restaurant(self, obj):
        oid = obj.restaurant_id
        if isObjectId(oid):
            try:
                link = reverse(
                    "admin:restaurant_pendingrestaurant_change", args=[oid])
                return format_html("<a href='{}' target='_blank' rel='noopener'>{}</a>", link, oid)
            except NoReverseMatch as e:
                return str(oid)
            except Exception as e:
                return str(oid)
        else:
            return ""

    link_to_restaurant.short_description = 'restaurant_id (link to restaurant)'


admin.site.register(RestaurantOwner, RestaurantOwnerAdmin)
