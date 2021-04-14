"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import url

from server.admin import admin_site
from sduser.utils import verify_email
from sduser.forms import SDPasswordChangeForm, SDPasswordResetForm

import restaurant
import article
import index
import auth
import sduser

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import datetime

urlpatterns = [
    path('email/', include('index.urls')),
    path('admin/password_change/',
         auth_views.PasswordChangeView.as_view(
             form_class=SDPasswordChangeForm,
             success_url=reverse_lazy('admin:password_change_done')
         ), name='password_change'),
    path('admin/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=SDPasswordResetForm,
        ),
        name='admin_password_reset',),
    path('admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',),
    path('admin/', admin_site.urls),
    path('auth/', include('auth.urls')),
    path('user/', include('sduser.urls')),
    path('subscriber/', include('subscriber_profile.urls')),
    path('owner/', include('restaurant_owner.urls')),
    path('article/', include('article.urls')),
    path('', include('restaurant.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Find Dining APIs",
      default_version='v2',
      description="Documentation of all APIs used for the Find Dining project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@finddining.ca"),
      license=openapi.License(name=str(datetime.datetime.now().year)+" Find Dining"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

if settings.DEBUG:
    doc_urls = [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        url(r'^redoc/#operation/POST%20/auth_refresh_create/$', sduser.backends.auth_refresh_view, name='schema-redoc'),
    ]
    urlpatterns.extend(doc_urls)

# prefix all URLpatterns with api/ i.e. api/urlpattern
urlpatterns = [
    #path('verification/', include('verify_email.urls')),
    path('verification/<uidb64>/<token>/',verify_email, name='verify_email'), 
    path('login/', index.views.angularLogIn, name="login"),
    path('api/', include(urlpatterns))]

'''
# prefix all URLpatterns with api/ i.e. api/urlpattern
urlpatterns = [
    path('api/', include(urlpatterns)),
    re_path(r'^(?!ng/).*$', include('index.urls')),]

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''