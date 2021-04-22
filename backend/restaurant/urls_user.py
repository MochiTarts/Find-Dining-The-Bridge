from django.urls import path
from restaurant import views

urlpatterns = [
    path('favourite/', views.UserFavView.as_view(), name='user_favourite'),
    path('favourite/<str:rest_id>/',
         views.FavRelationView.as_view(), name='remove_fav'),
]
