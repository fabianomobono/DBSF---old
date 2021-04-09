from django.urls import path, include
from .import views

urlpatterns = [
  path('', views.api, name='api_view'),
  path('users', views.users, name='user_api')
]