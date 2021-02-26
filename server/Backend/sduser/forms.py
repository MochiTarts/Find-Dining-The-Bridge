from django import forms
from .models import SDUser
#from django.contrib.auth.forms import UserCreationForm

# an instance is used for the second param of send_verification_email function
class SDUserCreateForm(forms.ModelForm):
    class Meta:
        model = SDUser
        fields = ('username', 'email', 'password', 'role',)
