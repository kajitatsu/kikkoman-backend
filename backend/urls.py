from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('all_restaurants/', views.all_restaurants, name='all_restaurants'),  # /backend/に対応
    path('search_restaurants/', views.search_restaurants, name='search_restaurants'),
    path('search_by_location/', views.search_by_location, name='search_by_location'),
    path('restaurant_count/', views.restaurant_count, name='restaurant_count'),
    path('search_with_location_and_filters/', views.search_with_location_and_filters, name='search_with_location_and_filters'),
]