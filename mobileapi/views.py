from django.shortcuts import render
from django.http import JsonResponse
from social.models import User, Get_info, Get_one_persons_posts

from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json


# Create your views here.
def api(request):
  users = User.objects.get(username='fabian')
  return JsonResponse({'answer': users.username })


@api_view()
def users(request):
  print('there was a request mado to rest_users')
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)
  

@api_view(["GET", "POST"])
def login(request):
  
  return JsonResponse({'gdf': 'sdf'})

# this gets called from the HomeScreen Component upon loading 
class HomeData(APIView):
    '''
    Return all the necessary for the home screen
    '''
    permission_classes = (IsAuthenticated,)
    def post(self, request):
       print(request.user)
       info = Get_info()
       r = info.info(request, 1)
       return Response({'hello': r})


# this gets called when the user views their own profile page, or another persons profile page
class One_persons_posts(APIView):
    '''
    get all the posts from one person
    '''

    # make sure the user is authenticated => has a token
    permission_classes = (IsAuthenticated,)
    def post(self, request):

        # get the name of the person that you need to load the posts from
        friend = json.loads(request.body.decode('UTF-8'))['friend']
        manager = Get_one_persons_posts()
        posts = manager.posts(friend, request, 1)
        return Response({'posts': posts})
