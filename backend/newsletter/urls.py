from django.urls import path
from newsletter.views import NLUserSignupView, NLUserDataView

urlpatterns = [
    path('signup/', NLUserSignupView.as_view(), name='newsletter_signup'),
    path('user/', NLUserDataView.as_view(), name='newsletter_user'),
]