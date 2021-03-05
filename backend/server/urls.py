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
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
import sduser
import verify_email
import index
from django.contrib.auth import views as auth_views
from sduser.backends import SDUserCookieTokenObtainPairView, SDUserCookieTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from google.views import GoogleView


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
    #path('auth/signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signin/', SDUserCookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', SDUserCookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/signup/', sduser.backends.signup),
    path('google/', GoogleView.as_view(), name='google'),
    #path('auth/signin/', obtain_jwt_token),
    #path('auth/refresh/', refresh_jwt_token),
    #path('auth/verify/', verify_jwt_token),
]

# prefix all URLpatterns with api/ i.e. api/urlpattern
urlpatterns = [
    path('verification/', include('verify_email.urls')),
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
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''