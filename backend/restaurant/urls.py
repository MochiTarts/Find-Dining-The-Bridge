from django.urls import path
from restaurant import views

urlpatterns = [
    path('dish/', views.DishView.as_view(), name='all_dishes'),
    path('dish/<string:rest_id>/', views.DishRestaurantView.as_view(), name='dish'),
    path('dish/p/<string:rest_id>/', views.PendingDishView(), name='pending_dish'),
    path('restaurant/<string:rest_id>/', views.RestaurantView.as_view(), name='restaurant'),
    path('restaurant/all/', views.AllRestaurantList.as_view(), name='all_restaurants'),
    path('restaurant/draft/', views.RestaurantDraftView.as_view(), name='restaurant_draft'),
    path('restaurant/submit/', views.RestaurantForApprovalView.as_view(), name='restaurant_for_approval'),
    path('restaurant/pending/<string:rest_id>/', views.PendingRestaurantView.as_view(), name='pending_restaurant'),
    path('restaurant/<string:rest_id>/favourited_users/', views.UserFavRestaurantView.as_view(), name='user_favs_restr'),
    path('user/<int:user_id>/favourite/', views.UserFavView.as_view(), name='user_favorite'),
    path('user/<int:user_id>/remove_favourite/<string:rest_id>/', views.FavRelationView.as_view(), name='remove_fav'),
]
