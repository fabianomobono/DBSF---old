from django.urls import path, include
from django.conf.urls import url
from . import views
from social.views import *


urlpatterns = [
    path("profile/<str:friend>", views.friends_profile, name='friends_profile'),
    path('like_a_post', Like_a_post.as_view(), name='like'),
    path('dislike_a_post', Dislike_a_post.as_view(), name='dislike'),
    path('', Index.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login'),
    path('index', Index.as_view(), name='index'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile', Profile.as_view(), name='profile'),
    path('change_profile_pic', views.change_profile_pic, name='upload_profile_pic'),
    path('create_new_post', Create_new_post.as_view(), name='create_new_post'),
    path('delete_post', views.delete_post_function, name='delete_post'),
    path('get_posts', views.get_posts, name='get_posts'), 
    path('request_friendship', views.request_friendship, name='add_friend'),
    path('get_f_requests', views.get_friend_requests, name='get_friend_requests'),
    path('confirm_friend_request', views.confirm_friend_request, name='confirm_friend_request'),
    path('ignore_friend_request', views.ignore_friend_request, name='ignore_friend_request'),
    path('unfriend', views.unfriend, name='unfriend'),
    path('friendship_id', views.get_friendship_id, name='get_friendship_id'),
    path('find_friendss', views.find_friendss, name='find_friendss'),
    path('get_own_posts', views.get_own_posts, name='get_my_posts'),
    path('comment', Comment_a_post.as_view(), name='comment'),
    path('sandbox', Sandbox.as_view(), name='go_nuts'),
    path('friends_profile_sandbox', Friends_profile_sandbox.as_view(), name='friends_profile_sandbox'),
    path('play', views.play, name='play'),
    path('set_new_password', views.set_new_password, name='set_new_password'),
    path('forgot_password', views.forgot_password, name='forgot_passsord'),
    path('google_auth_token', views.google_log_in, name='google_log_in'),
    url('google_login/', include('social_django.urls', namespace='social'))

   
]
