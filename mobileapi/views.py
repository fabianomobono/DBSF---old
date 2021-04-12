from django.shortcuts import render
from django.http import JsonResponse
from social.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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
  data = json.loads(request.body.decode("utf-8")) 
  print(data)
  return JsonResponse({'gdf': 'sdf'})


class HomeData(APIView):
    def post(self, request):
       return Response({'hello': request.user})
