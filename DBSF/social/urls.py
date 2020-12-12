from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='login'),
    path('login', views.login_view, name='login'),
    path('index', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change_profile_pic', views.change_profile_pic, name='upload_profile_pic')
]
