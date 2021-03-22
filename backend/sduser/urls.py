from django.urls import path
from sduser import views

urlpatterns = [
    path('edit/', views.editView.as_view(), name="edit"),
    path('deactivate/', views.deactivateView.as_view(), name="deactivate"),
]
