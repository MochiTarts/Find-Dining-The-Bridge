from django.urls import path

from . import views

urlpatterns = [
    #path('', views.angularIndex, name='index'),
    path('', views.indexView.as_view(), name='index'),
    path('all', views.indexView.as_view(), name='all'),
    path('user', views.indexView.as_view(), name='user'),
    path('ro', views.indexView.as_view(), name='ro'),
]