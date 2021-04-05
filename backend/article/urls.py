from django.urls import path
from article import views

urlpatterns = [
    path('all/', views.ArticleList.as_view(), name='all_articles'),
]