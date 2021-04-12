from django.contrib import admin
from django.contrib.auth import signals
from django.contrib.auth import authenticate, login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView
from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from login_audit.forms import LoginForm


class NewLoginView(LoginView):

    def get_redirect_url(self):

        if self.request.method == "POST" and self.request.user.get_username()\
                and not self.request.user.default_pwd_updated:
            redirect_to = reverse("admin:password_change")
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, '')
            )
        return redirect_to

    #http_method_names = ['post']


class NewAdminSite(AdminSite):
    # site_header = site_title = gettext_lazy("Find Dining Admin Site")
    login_form = LoginForm

    def __init__(self, name="admin"):
        super().__init__(name)

    # Display the login form for the given HttpRequest.
    @never_cache
    def login(self, request, extra_context=None):

        # already logged in
        if request.method == 'GET' and self.has_permission(request):
            if request.user.get_username() and not request.user.default_pwd_updated:
                # default password not changed, force to reset password page (password_change view)
                path = reverse('admin:password_change', current_app=self.name)
                # path = "admin/password_change"
            else:
                # redirect to admin index
                path = reverse('admin:index', current_app=self.name)

            return HttpResponseRedirect(path)

        context = {
            **self.each_context(request),
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            'username': request.user.get_username(),
        }
        if (REDIRECT_FIELD_NAME not in request.GET and
                REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse(
                'admin:index', current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        # use NewLoginView
        return NewLoginView.as_view(**defaults)(request)

    def using_default_password(self, request):
        if self.has_permission(request) and request.user.get_username() and not request.user.default_pwd_updated:
            return True
        return False

    def each_context(self, request):
        context = super().each_context(request)
        context["force_pwd_change"] = self.using_default_password(request)
        return context

    @never_cache
    def index(self, request, extra_context=None):
        if request.user.get_username() and not request.user.default_pwd_updated:
            # if default password not updated, force to password_change page
            context = self.each_context(request)
            context.update(extra_context or {})
            return self.password_change(request, context)
        return super().index(request, extra_context)


# Create an instance of admin_site object from NewAdminSite
admin_site = NewAdminSite(name='admin')
# replace admin.site with my custom admin_site
admin.site = admin_site

# customization on the admin site (global)
# header
admin.site.site_header = "Find Dining Administration"
# url for view_site
admin.site.site_url = "https://localhost:4200"
#admin.site.site_url = "https://finddining.ca"
main_site_url = settings.MAIN_SITE_URL
if main_site_url:
    admin.site.site_url = main_site_url

# title suffix
# admin.site.site_title = "Administration"
# Title of admin index page
admin.site.index_title = "Find Dining Administration"
