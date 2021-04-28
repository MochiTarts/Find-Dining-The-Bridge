from djongo import models
from django import forms
from collections import OrderedDict


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


class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
