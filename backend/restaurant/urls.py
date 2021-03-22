from django.urls import path
from restaurant import views

urlpatterns = [
    path('dish/', views.DishView.as_view(), name='all_dishes'),
    path('dish/<string:rest_id>', views.DishRestaurantView.as_view(), name='dish'),
    path('dish/p/<string:rest_id>', views.PendingDishView(), name='insert_pending_dish'),
    path('restr/<string:rest_id>', views.RestaurantView.as_view(), name='get_restaurant'),
    path('restr/all/', views.AllRestaurantList.as_view(), name='get_all_restaurants'),
    path('restr/draft/', views.RestaurantDraftView.as_view(), name='insert_restaurant_draft'),
    path('restr/submit/', views.RestaurantForApprovalView.as_view(), name='insert_restaurant_for_approval'),
    path('restr/pending/', views.PendingRestaurantView.as_view(), name='get_pending_restaurant'),
    path('restr/<string:rest_id>/favourited_users/', views.UserFavRestaurantView.as_view(), name='get_user_favs_restr'),
    path('user/<int:user_id>/favourite/', views.UserFavView.as_view(), name='user_favorite'),
    path('user/<int:user_id>/remove_favourite/<string:rest_id>', views.FavRelationView.as_view(), name='remove_fav'),
]
