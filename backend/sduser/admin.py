from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password

#from django.contrib.auth.admin import UserAdmin
from sduser.forms import AdminForm
from utils.filters import InputFilter, EmailFilter, UsernameFilter

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'activated', 'role', 'is_blocked', 'is_staff', 'is_superuser', 'last_login', 'pwd_update_time')
    list_filter = (EmailFilter, UsernameFilter, 'is_staff', 'is_superuser', 'is_blocked',)

    class Meta:
        # for some reason setting this is not enough, need to override get_form as well
        form = AdminForm

    def get_form(self, request, obj=None, **kwargs):
        '''
        if request.user.is_superuser:
            kwargs['form'] = MySuperuserForm
        '''
        kwargs['form'] = AdminForm
        return super().get_form(request, obj, **kwargs)
    # a field to keep track whether this user has activated the account (has reset the password upon log in)
    def activated(self, obj):
        return obj.default_pwd_updated
    
    def save_model(self, request, obj, form, change):
        # need to make sure the pk is a required field when creating a new admin user
        # otherwise we need to check its existence for now
        if obj.pk:
            user = User.objects.get(pk=obj.pk)
            # Check first the case in which the password is not encoded, then check in the case that the password is encode
            if not (check_password(form.data['password'], user.password) or user.password == form.data['password']):
                obj.password = make_password(obj.password)
            else:
                obj.password = user.password
        else:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
    '''
    # No longer needed as I have nullify the confirmation field during clean_password on form saves
    # but keep the code here if at any point we want to modify the history directly...
    # (hack) filter out 'password2' by modifying the rendered content of template response
    def history_view(self, request, object_id, extra_context=None):
        #extra_context = extra_context or {}
        templateResponse = super().history_view(
            request, object_id, extra_context=extra_context,
        )
        if templateResponse is None:
            return 
        # this is needed for content but not rendered_content
        #templateResponse.render()

        # only passwrod2 changed => nothing else changed
        new_rendered_content = templateResponse.rendered_content.replace('Changed password2.', 'No fields changed.')
        # password2 is for validation only, not meaningful in history
        new_rendered_content = new_rendered_content.replace('password2', '')
        templateResponse.content = new_rendered_content

        return templateResponse
    '''

admin.site.register(User, UserAdmin)