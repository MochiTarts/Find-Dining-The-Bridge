from django.urls import path
from restaurant import views

urlpatterns = [
    path('all/', views.DishList.as_view(), name='all_dishes'),
    path('approved/<str:rest_id>/',
         views.DishRestaurantView.as_view(), name='dish'),
    path('pending/', views.PendingDishView.as_view(), name='pending_dish'),
    path('pending/<str:dish_id>/',
         views.PendingDishModifyDeleteView.as_view(), name='pending_dish_edit'),
    path('media/<str:dish_id>/', views.DishMediaView.as_view(), name='dish_media'),
]
