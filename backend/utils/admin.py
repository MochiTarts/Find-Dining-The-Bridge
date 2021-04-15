from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from bson import ObjectId


def isObjectId(oid):
    return ObjectId.is_valid(oid)

# custom input filter (parent) class that works with the default list filter (can create custom filter by subclassing it)


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # dummy return (required to show the filter)
        return ((),)

    def choices(self, changelist):
        # grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


''' custom filters'''

# email filter (not exact match but 'contains' for wider usability)


class EmailFilter(InputFilter):
    parameter_name = 'email'
    title = _('email')

    def queryset(self, request, queryset):
        if self.value() is not None:
            email = self.value()

            return queryset.filter(
                Q(email__icontains=email)
            )

# email filter (not exact match but 'contains' for wider usability)


class UsernameFilter(InputFilter):
    parameter_name = 'username'
    title = _('username')

    def queryset(self, request, queryset):
        if self.value() is not None:
            username = self.value()

            return queryset.filter(
                Q(username__icontains=username)
            )


# owner name filter (not exact match but 'contains' for wider usability)
class OwnerNameFilter(InputFilter):
    parameter_name = 'owner_name'
    title = _('owner name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            owner_name = self.value()

            return queryset.filter(
                Q(owner_first_name__icontains=owner_name) |
                Q(owner_last_name__icontains=owner_name) |
                Q(owner_prefer_name__icontains=owner_name)
            )


# name filter (not exact match but 'contains' for wider usability)
class NameFilter(InputFilter):
    parameter_name = 'name'
    title = _('name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()

            return queryset.filter(
                Q(name__icontains=name)
            )

# filter won't work until we change the db schema (change price field from string to number)
# price max filter (upper bound)


class PriceMaxFilter(InputFilter):
    parameter_name = 'price'
    title = _('price (maximum)')

    def queryset(self, request, queryset):
        if self.value() is not None:
            price = self.value()
            if price.isnumeric:
                return queryset.filter(
                    Q(price__lt=float(price))
                )

# price min filter (lower bound)


class PriceMinFilter(InputFilter):
    parameter_name = 'price'
    title = _('price (minimum)')

    def queryset(self, request, queryset):
        if self.value() is not None:
            price = self.value()
            if price.isnumeric:
                return queryset.filter(
                    Q(price__gt=float(price))
                )
