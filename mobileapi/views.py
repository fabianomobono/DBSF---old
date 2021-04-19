from django.shortcuts import render
from django.http import JsonResponse
from social.models import User, Get_info, Get_one_persons_posts
from django.db import IntegrityError
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import json
import arrow


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


class SignUpView(APIView):
    '''
    this handles the sign up process from the mobile app
    '''
    def post(self, request):
        danger = ['"', "'"]
        try:
            print('trying')
            data = json.loads(request.body.decode('UTF-8'))
            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            confirmation = data['confirmation']
            print('this is dob')
            dob = arrow.get(data['dob'])
            
            print(dob)

            # check if all fields are not empty strings
            if username == '' or first_name == '' or last_name == '' or email == '' or dob == '' or password == '' or confirmation == '':
                return Response({'response': 'you must fill out all fields'})

            # check if all contain spaces
            elif ' ' in username or ' ' in first_name or ' ' in last_name or ' ' in email  or ' 'in password:
                return Response({'response': 'spaces are not allowed as characters'}) 

            # check if the fields contain dangerous characeters
            elif any(x in username for x in danger) or any(x in first_name for x in danger) or any(x in last_name for x in danger) or any(x in email for x in danger) or any(x in password for x in danger):
                return Response({'response': 'no single or double quotes'}) 


            # check if password and confirmation match
            elif password != confirmation:
                return Response({'response': 'Passwords do not match'})

            else:
                try:
                    # try to create a new user
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, dob=dob.format('YYYY-MM-DD'))
                    
                    # get the new users token 
                    token = Token.objects.get(user=user)
                    
                    # HURRAYYY user and token have been created...sending back token
                    return Response({'response': token.key})
            
                # if the username already exists
                except IntegrityError:
                    return Response({'response': 'username is taken'})
            
            return Response({'response': 'so far so good'})
           
        except:
            return Response({'response': 'not all fields where provided...or something else went wrong'})
        
       

          
      
          
      