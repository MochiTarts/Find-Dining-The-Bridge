from django.urls import path
from restaurant import views

urlpatterns = [
    path('all/', views.AllRestaurantList.as_view(), name='all_restaurants'),
    path('approved/<str:rest_id>/',
         views.RestaurantView.as_view(), name='restaurant'),
    path('draft/', views.RestaurantDraftView.as_view(), name='restaurant_draft'),
    path('submit/', views.RestaurantForApprovalView.as_view(),
         name='restaurant_for_approval'),
    path('pending/', views.PendingRestaurantView.as_view(),
         name='pending_restaurant'),
    path('<str:rest_id>/favourited_users/',
         views.UserFavRestaurantView.as_view(), name='user_favs_restr'),
    path('traffic/<str:format_type>/',
         views.RestaurantsAnalyticsDataView.as_view(), name='restaurants_traffic'),
    path('<str:rest_id>/traffic/<str:format_type>/',
         views.RestaurantAnalyticsDataView.as_view(), name='restaurant_traffic'),
    path('post/', views.PostView.as_view(), name='restaurant_post'),
    path('post/<str:post_id>/', views.PostDeleteView.as_view(),
         name='restaurant_post_delete'),
    path('public/post/<str:rest_id>/', views.PublicPostView.as_view(),
         name='restaurant_public_post'),
    path('media/', views.RestaurantMediaView.as_view(), name='restaurant_media'),
    path('reverse_geocode/', views.ReverseGeocodeView.as_view(), name='reverse_geocode'),
]
