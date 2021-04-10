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

from sduser.backends import verify_email

from server.admin import admin_site
from sduser.forms import SDPasswordChangeForm, SDPasswordResetForm

import restaurant
import article
import index
import auth

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