from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.index, name='all'),
    path('user', views.index, name='user'),
    path('ro', views.index, name='ro'),
]