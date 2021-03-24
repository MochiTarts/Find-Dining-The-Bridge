from django.urls import path
from restaurant_owner import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('profile/', views.RestaurantOwnerView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/', views.RestaurantOwnerView.as_view(), name="profile_get")
]