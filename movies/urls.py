from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("search/", views.search, name="search"),
    path("api/trendings/", views.view_trendings_results, name="trendings"),
    # path("movie/<int:movie_id>/", views.view_movie_detail, name="moviedetail"),
    # path('add_to_watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    # path('rate_movie/<int:movie_id>/', views.rate_movie, name='rate_movie'),

    path('movie/<int:movie_id>/', views.view_movie_detail, name='view_movie_detail'),
    path('movie/<int:movie_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),

    # path("tv/<int:tv_id>/", views.view_tv_detail, name="tvdetail"),
    path('tv/<int:tv_id>/', views.view_tv_detail, name='view_tv_detail'),
    path('tv/<int:tv_id>/add_to_watchlist/', views.add_tv_to_watchlist, name='add_tv_to_watchlist'),
    path('tv/<int:tv_id>/rate/', views.rate_tv_show, name='rate_tv_show'),
]
