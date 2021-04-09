from django.shortcuts import render
from django.http import JsonResponse
from social.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
  
