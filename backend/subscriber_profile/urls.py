from django.urls import path
from subscriber_profile import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name="signup"),
    path('profile/', views.SubscriberProfileView.as_view(), name="profile")
]
