from django.urls import path
from restaurant import views

urlpatterns = [
    path('dish/all/', views.DishList.as_view(), name='all_dishes'),
    path('dish/approved/<str:rest_id>/', views.DishRestaurantView.as_view(), name='dish'),
    path('dish/pending/', views.PendingDishView.as_view(), name='pending_dish'),
    path('dish/pending/<str:dish_id>/', views.PendingDishModifyDeleteView.as_view(), name='pending_dish_edit'),
    path('dish/media/<str:dish_id>/', views.DishMediaView.as_view(), name='dish_media'),
    path('restaurant/all/', views.AllRestaurantList.as_view(), name='all_restaurants'),
    path('restaurant/approved/<str:rest_id>/', views.RestaurantView.as_view(), name='restaurant'),
    path('restaurant/draft/', views.RestaurantDraftView.as_view(), name='restaurant_draft'),
    path('restaurant/submit/', views.RestaurantForApprovalView.as_view(), name='restaurant_for_approval'),
    path('restaurant/pending/', views.PendingRestaurantView.as_view(), name='pending_restaurant'),
    path('restaurant/<str:rest_id>/favourited_users/', views.UserFavRestaurantView.as_view(), name='user_favs_restr'),
    path('restaurant/traffic/<str:format_type>/', views.RestaurantsAnalyticsDataView.as_view(), name='restaurants_traffic'),
    path('restaurant/<str:rest_id>/traffic/<str:format_type>/', views.RestaurantAnalyticsDataView.as_view(), name='restaurant_traffic'),
    path('user/favourite/', views.UserFavView.as_view(), name='user_favourite'),
    path('user/favourite/<str:rest_id>/', views.FavRelationView.as_view(), name='remove_fav'),
    path('restaurant/post/', views.PostView.as_view(), name='restaurant_post'),
    path('restaurant/post/<str:post_id>/', views.PostDeleteView.as_view(), name='restaurant_post_delete'),
    path('restaurant/public/post/<str:rest_id>/', views.PublicPostView.as_view(), name='restaurant_public_post'),
    path('restaurant/media/', views.RestaurantMediaView.as_view(), name='restaurant_media'),
]
