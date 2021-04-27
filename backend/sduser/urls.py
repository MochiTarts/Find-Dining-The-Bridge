from django.urls import path
from sduser import views

urlpatterns = [
    path('edit/', views.SDUserEditView.as_view(), name="edit"),
    path('change_password/', views.SDUserChangePasswordView.as_view(),
         name="change_password"),
    path('deactivate/', views.DeactivateView.as_view(), name="deactivate"),
    path('nearby/', views.NearbyRestaurantsView.as_view(), name="nearby"),
]
