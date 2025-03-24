from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('all_restaurants/', views.all_restaurants, name='all_restaurants'),  # /backend/に対応
]