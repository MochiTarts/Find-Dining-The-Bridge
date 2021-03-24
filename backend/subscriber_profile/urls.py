from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name="signup"),
    path('profile/', views.SubscriberProfileView.as_view(), name="profile"),
    path('consent_status/', views.ConsentStatusView.as_view(), name="consent status"),
    path('nearby/<int:user_id>/', views.NearbyRestaurantsView.as_view(), name='nearby')
]
