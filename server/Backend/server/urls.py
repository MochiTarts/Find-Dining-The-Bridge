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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
import sduser
import verify_email

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', include('index.urls')),
    path('admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
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
    path('admin/', admin.site.urls),
    path('verification/', include('verify_email.urls')),
    #path('api-token-auth/', obtain_jwt_token),
    path('auth/signin/', obtain_jwt_token),
    path('auth/signup/', sduser.backends.signup),
    path('aith/refresh/', refresh_jwt_token),
]

# prefix all URLpatterns with api/ i.e. api/urlpattern
urlpatterns = [path('api/', include(urlpatterns))]

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
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''