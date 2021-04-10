from django.urls import path, include
from .import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path('', views.api, name='api_view'),
  path('users', views.users, name='user_api'),
  path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
  path('login', views.login, name='fake_login')
]