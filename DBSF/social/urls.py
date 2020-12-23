from django.urls import path
from . import views


urlpatterns = [
    path("profile/<str:friend>", views.friends_profile, name='friends_profile'),
    path('', views.index, name='login'),
    path('login', views.login_view, name='login'),
    path('index', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change_profile_pic', views.change_profile_pic, name='upload_profile_pic'),
    path('create_new_post', views.create_new_post, name='create_new_post'),
    path('delete_post', views.delete_post_function, name='delete_post'),
    path('get_posts', views.get_posts, name='get_posts'),   
]
