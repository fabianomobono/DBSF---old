from django.shortcuts import render
from django.http import JsonResponse
from social.models import User, Get_info, Get_one_persons_posts, Post, Comment, Friendship, Like, Dislike
from django.db import IntegrityError
from .serializers import UserSerializer, CommentSerializer
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


# this handles the sign up from the mobile app... the route is mobileSignUp
class SignUpView(APIView):
    '''
    this handles the sign up process from the mobile app
    '''
    def post(self, request):
        danger = ['"', "'"]
        try:          
            data = json.loads(request.body.decode('UTF-8'))          
            username = data['username']          
            first_name = data['first_name']         
            last_name = data['last_name']           
            email = data['email']         
            password = data['password']          
            confirmation = data['confirmation']          
            dob = arrow.get(data['dob'])
               
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
                    return Response({'response': 'HURRAYYY user and token have been created...sending back token', 'token': token.key})
            
                # if the username already exists
                except IntegrityError:
                    return Response({'response': 'username is taken'})
            
            return Response({'response': 'so far so good'})
           
        except:
            return Response({'response': 'not all fields where provided...or something else went wrong'})
        

# create a new post 
class Create_new_post(APIView):
    permission_classes = (IsAuthenticated,)     

    def post(self, request):
        # get the data from the 
        text = json.loads(request.body.decode('UTF-8'))['text']
        new_post = Post.objects.create(text=text, author=request.user)

        # create an arrow object
        time_arrow = arrow.utcnow()
        response = {
            'author': new_post.author.username, 
            'date': time_arrow.humanize(), 
            'id': new_post.id, 
            'text': text,
            'comments': []} 
        return Response({'response': response})


# comment a post API
class Comment_a_post(APIView):

    # restrict access to users that have a token
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print('working on commenting')
        data = json.loads(request.body.decode('UTF-8'))
        text = data['text']
        post = Post.objects.get(pk=data['post_id'])
        user = request.user

        comment = Comment(text=text, commentator=user, post=post)
        comment.save()

        return Response({
            "id": comment.id, 
            "text": comment.text, 
            "commentator": request.user.username, 
            "profile_pic": request.user.profile_pic.url, 
            "date": comment.date,
            "likes": comment.likes
        })
          

class FindFriends(APIView):
    
    # restrict access to authenticated users => they need to have token => they need to be logged in
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        search_term = json.loads(request.body)['search_term']
        results = User.objects.filter(username__contains=search_term)
        users = []

        for user in results:

            # check if current user and user are friends
            requested = Friendship.objects.filter(sender=request.user, receiver=user)
            received = Friendship.objects.filter(sender=user, receiver=request.user)

            # if a requested Friendship object exists check the friendship status
            if requested.count() != 0:

                # This logic is used to determine what the Friend request button needs to display -- right now this feature is not active
                if requested[0].pending == True:
                    users.append({'user': user.username, 'first': user.first_name, 'last': user.last_name, 'status': 'Pending', 'profile_pic': user.profile_pic.url, 'rejected': False})
                else:
                    users.append({'user': user.username, 'first': user.first_name, 'last': user.last_name, 'status': 'Friends', 'profile_pic': user.profile_pic.url, 'rejected': requested[0].rejected})


            # if a received Friendship object exists check the friendship status
            elif received.count() != 0:

                # This logic is used to determine what the Friend request button needs to display -- right now this feature is not active
                if received[0].pending == True:
                    users.append({'user': user.username, 'first': user.first_name, 'last': user.last_name, 'status': 'Pending', 'profile_pic': user.profile_pic.url , 'rejected': False})
                else:
                    users.append({'user': user.username, 'first': user.first_name, 'last': user.last_name, 'status': 'Friends', 'profile_pic': user.profile_pic.url, 'rejected': received[0].rejected})

            # if they are not friends
            else:
                users.append({'user': user.username, 'first': user.first_name, 'last': user.last_name, 'status': "not friends", 'profile_pic': user.profile_pic.url})

        return Response({'response': users})


# update the profile pic
class UpdateProfilePic(APIView):

    # make sure the request is coming from an authenticated user
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.FILES)
       
        picture = request.FILES['profile_pic']
        user = User.objects.get(username=request.user)
        user.profile_pic = picture
        user.save()
        return Response({'response': user.profile_pic.url})


class GetCommentsForPost(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        post_id = json.loads(request.body.decode('UTF-8'))['post_id']
        comments = Comment.objects.filter(post=(Post.objects.get(id=post_id)))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
