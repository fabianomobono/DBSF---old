from django.urls import path, include
from .import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
  path('', views.api, name='api_view'),
  path('users', views.users, name='user_api'), 
  path('login', views.login, name='fake_login'),
  path('get_info', HomeData.as_view(), name='startapp_info'),
  path('one_persons_posts', One_persons_posts.as_view(), name='one_persons_posts'),
]