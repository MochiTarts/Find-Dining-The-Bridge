
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from restaurant.models import Restaurant, PendingRestaurant, RestaurantPost
from restaurant.enum import MediaType, RestaurantSaveLocations, FoodSaveLocations
from utils.validators import validate_profane_content

# for ordering and hiding info


class RestaurantAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Restaurant
        fields = ('name', 'years', 'owner_first_name', 'owner_last_name', 'owner_preferred_name',
                  'categories', 'sysAdminComments', 'address',
                  'streetAddress2', 'streetAddress3', 'postalCode',
                  'phone', 'email', 'pricepoint', 'cuisines', 'offer_options', 'dineinPickupDetails', 'deliveryDetails', 'locationNotes', 'web_url',
                  'facebook', 'twitter', 'instagram', 'bio', 'GEO_location', 'cover_photo_url', 'logo_url',
                  'restaurant_image_url', 'open_hours', 'payment_methods', 'full_menu_url', )


class RestaurantMediaForm(forms.Form):
    """ For validating form data of restaurant media API requests """
    media_type = forms.ChoiceField(choices=MediaType.choices(), required=True)
    save_location = forms.ChoiceField(
        choices=RestaurantSaveLocations.choices(), required=True)
    media_file = forms.FileField(required=False)
    media_link = forms.CharField(required=False)
    submit_for_approval = forms.ChoiceField(
        choices=(('True', 'True'), ('False', 'False')))


class RestaurantImageDeleteForm(forms.Form):
    """ For validating form data of restaurant image(s) deletion API requests """
    restaurant_images = forms.CharField(required=True)


class FoodMediaForm(forms.Form):
    """ For validating form data of dish media API requestes """
    media_type = forms.ChoiceField(choices=MediaType.choices(), required=True)
    save_location = forms.ChoiceField(
        choices=FoodSaveLocations.choices(), required=True)
    media_file = forms.FileField(required=True)
