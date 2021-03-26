from django.contrib import admin
from django.urls.exceptions import NoReverseMatch
from django.urls import reverse
from django.utils.html import format_html

from subscriber_profile.models import SubscriberProfile
from sduser.models import SDUser
from utils.filters import UserIDFilter


class SubscriberProfileAdmin(admin.ModelAdmin):
    """ Admin Model for SubscriberProfile """
    list_filter = (UserIDFilter, 'consent_status',)
    list_display = ('user_id', 'first_name', 'last_name', 'link_to_user', 'phone', 'postalCode',
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


admin.site.register(SubscriberProfile, SubscriberProfileAdmin)
