from django.urls import path

from sduser.backends import SDUserSignupView, SDUserCookieTokenObtainPairView, SDUserCookieTokenRefreshView
from sduser.views import (
    SDUserPasswordResetView,
    SDUserPasswordResetConfirmView,
    SDUserPasswordResetCompleteView,
    SDUserResentVerificationEmailView,
    SDUserLogoutView,
)
from oauth2 import views as external_auth_view

from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('signin/', SDUserCookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('logout/', SDUserLogoutView.as_view(),
         name='user_logout'),
    path('refresh/', SDUserCookieTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', SDUserSignupView.as_view(), name='signup'),
    path('password_reset/', SDUserPasswordResetView.as_view(),
         name='password_reset_user'),
    path('password_reset/<uidb64>/<token>/',
         SDUserPasswordResetConfirmView.as_view(), name='password_reset_confirm_user',),
    path('password_reset/done/', SDUserPasswordResetCompleteView.as_view(),
         name='password_reset_complete_user',),
    path('resend_verification_email/', SDUserResentVerificationEmailView.as_view(),
         name="resent_verification_email"),
    path('google/', external_auth_view.GoogleView.as_view(), name='google'),
    path('facebook/', external_auth_view.FacebookView.as_view(), name='google'),
]
