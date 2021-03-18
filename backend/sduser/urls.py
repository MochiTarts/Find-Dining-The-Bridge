from django.urls import path
from sduser import views

urlpatterns = [
    path('deactivate/', views.deactivateView.as_view(), name="deactivate"),
]
