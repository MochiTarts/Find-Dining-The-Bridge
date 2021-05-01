from djongo import models
from django import forms
from collections import OrderedDict


# To display CustomListField type fields on admin site properly
class StringListField(forms.CharField):
    def prepare_value(self, value):
        if type(value[0]) is OrderedDict:
            d = value[0]
            image_dict = {}
            for key, value in d.items():
                image_dict[key] = value
            return image_dict
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]


# Uses djongo's builtin ListField with formfield of the above custom
# StringListField so these database model fields can be displayed on
# the admin site properly
class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
