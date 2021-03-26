from django.urls import path

from index import views

urlpatterns = [
    path('send/', views.EmailView.as_view(), name='send_email'),
]