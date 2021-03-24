
from django import forms
from django.forms import ModelForm
from restaurant.models import Restaurant
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# for ordering and hiding info
class RestaurantAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Restaurant
        fields = ('name', 'years', 'owner_first_name', 'owner_last_name', 'owner_preferred_name',
                  'owner_story', 'owner_picture_url', 'categories', 'sysAdminComments', 'address',
                  'streetAddress2', 'streetAddress3', 'postalCode',
                  'phone', 'email', 'pricepoint', 'cuisines', 'offer_options', 'dineinPickupDetails', 'deliveryDetails', 'locationNotes', 'web_url',
                  'facebook', 'twitter', 'instagram', 'bio', 'GEO_location', 'cover_photo_url', 'logo_url',
                  'restaurant_image_url', 'open_hours', 'payment_methods', 'full_menu_url', )

