from django.urls import path
from sduser import views

urlpatterns = [
    path('deactivate/', views.deactivate_user, name="deactivate"),
]
