from django.urls import path
from restaurant_owner import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="owner_signup"),
    path('profile/<int:user_id>/', views.RestaurantOwnerView.as_view(), name="owner_profile"),
    path('nearby/<int:user_id>/', views.NearbyRestaurantsView.as_view(), name="nearby")
]