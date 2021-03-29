from django.urls import path
from sduser.backends import signup, SDUserCookieTokenObtainPairView, SDUserCookieTokenRefreshView
from sduser.views import SDUserPasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from oauth2 import views as external_auth_view

urlpatterns = [
    #path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/', SDUserCookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', SDUserCookieTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', signup),
    path('password_reset/', SDUserPasswordResetView.as_view(), name='password_reset'),
    path('google/', external_auth_view.GoogleView.as_view(), name='google'),
    path('facebook/', external_auth_view.FacebookView.as_view(), name='google'),
]