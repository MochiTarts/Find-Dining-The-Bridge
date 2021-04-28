
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from restaurant.models import Restaurant, PendingRestaurant, RestaurantPost, Food
from restaurant.enum import MediaType, RestaurantSaveLocations, FoodSaveLocations
from utils.validators import validate_profane_content

# for ordering and hiding info


class RestaurantAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Restaurant
        fields = ('name', 'years', 'owner_first_name', 'owner_last_name', 'owner_preferred_name',
                  'categories', 'address',
                  'streetAddress2', 'streetAddress3', 'postalCode',
                  'phone', 'email', 'pricepoint', 'cuisines', 'offer_options', 'dineinPickupDetails', 'deliveryDetails', 'locationNotes', 'web_url',
                  'facebook', 'twitter', 'instagram', 'bio', 'GEO_location', 'cover_photo_url', 'logo_url',
                  'restaurant_image_url', 'open_hours', 'sysAdminComments', 'payment_methods', 'full_menu_url', )
        widgets = {
            'owner_first_name': forms.TextInput(attrs={'size': 100}),
            'owner_last_name': forms.TextInput(attrs={'size': 100}),
            'owner_preferred_name': forms.TextInput(attrs={'size': 100}),
            'categories': forms.TextInput(attrs={'size': 100}),
            'cuisines': forms.TextInput(attrs={'size': 200}),
            'offer_options': forms.TextInput(attrs={'size': 200}),
            'restaurant_image_url': forms.TextInput(attrs={'size': 200}),
            'locationNotes': forms.Textarea(attrs={'rows': 8, 'cols': 99}),
            'sysAdminComments': forms.Textarea(attrs={'rows': 8, 'cols': 99})
        }


class DishAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Food
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 41})
        }


class RestaurantMediaForm(forms.Form):
    """ For validating form data of restaurant media API requests """
    media_type = forms.ChoiceField(choices=MediaType.choices(), required=True)
    save_location = forms.ChoiceField(
        choices=RestaurantSaveLocations.choices(), required=True)
    media_file = forms.FileField(required=False)
    image_captions = forms.CharField(required=False)
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
