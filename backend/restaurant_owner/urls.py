from django.urls import path
from restaurant_owner import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="owner_signup"),
    path('profile/', views.RestaurantOwnerView.as_view(), name="owner_profile"),
]
