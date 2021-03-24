from django.urls import path
from restaurant import views

urlpatterns = [
    path('dish/all/', views.DishList.as_view(), name='all_dishes'),
    path('dish/approved/<str:rest_id>/', views.DishRestaurantView.as_view(), name='dish'),
    path('dish/pending/<str:rest_id>/', views.PendingDishView.as_view(), name='pending_dish'),
    path('dish/pending/<str:rest_id>/<str:dish_id>/', views.PendingDishView.as_view(), name='pending_dish_edit'),
    path('restaurant/all/', views.AllRestaurantList.as_view(), name='all_restaurants'),
    path('restaurant/approved/<str:rest_id>/', views.RestaurantView.as_view(), name='restaurant'),
    path('restaurant/draft/', views.RestaurantDraftView.as_view(), name='restaurant_draft'),
    path('restaurant/draft/<str:rest_id>/', views.RestaurantDraftView.as_view(), name='restaurant_draft_edit'),
    path('restaurant/submit/', views.RestaurantForApprovalView.as_view(), name='restaurant_for_approval'),
    path('restaurant/submit/<str:rest_id>/', views.RestaurantForApprovalView.as_view(), name='restaurant_for_approval_edit'),
    path('restaurant/pending/<str:rest_id>/', views.PendingRestaurantView.as_view(), name='pending_restaurant'),
    path('restaurant/<str:rest_id>/favourited_users/', views.UserFavRestaurantView.as_view(), name='user_favs_restr'),
    path('restaurant/<str:rest_id>/traffic/', views.AnalyticsDataView.as_view(), name='restaurant_traffic'),
    path('user/favourite/', views.UserFavView.as_view(), name='user_favourite'),
    path('user/<int:user_id>/favourite/', views.UserFavView.as_view(), name='user_favourite'),
    path('user/<int:user_id>/remove_favourite/<str:rest_id>/', views.FavRelationView.as_view(), name='remove_fav'),
    path('analytics/access_token/', views.AnalyticsAccessTokenView.as_view(), name='analytics_access_token'),
]
