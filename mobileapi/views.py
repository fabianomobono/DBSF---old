from django.shortcuts import render
from django.http import JsonResponse
from social.models import User, Get_info

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


class HomeData(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
       print(request.user)
       info = Get_info()
       r = info.info(request, 1)
       return Response({'hello': r})
