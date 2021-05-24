from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse
from django.urls import reverse
from social.models import User, Get_info, Get_one_persons_posts, Post, Comment, Friendship, Like, Dislike, Message
from django.db import IntegrityError
from .serializers import UserSerializer, CommentSerializer, MessageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import json
import arrow
import datetime

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
        try:
            friend = User.objects.get(username=(json.loads(request.body.decode('UTF-8'))['friend']))
        
        except:
            return Response({'posts': [], 'status': 'no user'})

        manager = Get_one_persons_posts()
        posts = manager.posts(friend, request, 1)

        # get Friendship status between the current user and the friend
        # Friendships can be reqeusted or received so we have to check both cases
        sent = Friendship.objects.filter(sender=request.user, receiver=(User.objects.get(username=friend)))
        received = Friendship.objects.filter(sender=(User.objects.get(username=friend)), receiver=request.user)

        if (len(sent) == 0 and len(received) == 0):
            return Response({'posts': posts, 'status': 'not friends'})

        elif(len(sent) > 0):

            if(sent[0].are_they_friends):
                return Response({'posts': posts, 'status': 'friends'})

            if(sent[0].pending or sent[0].rejected):
                return Response({'posts': posts, 'status': 'pending or rejected'})

        elif(len(received) > 0):

            if(received[0].are_they_friends):
                return Response({'posts': posts, 'status': 'friends'})

            if(received[0].pending or received[0].rejected):
                return Response({'posts': posts, 'status': 'pending or rejected'})

        return Response({'posts': posts, 'status': 'something went wrong with the statuses'})


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
                    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, dob=dob.format('YYYY-MM-DD'))
                    
                    # get the new users token 
                    token = Token.objects.get(user=user)
                    
                    # HURRAYYY user and token have been created...sending back token

                    # send an email to the new users email address
                    send_mail(
                        'You signed up',
                        'Hi there, you requested data from the server.',
                        'dbsfmanager@gmail.com',
                        ['fabian.omobono@gmail.com'],
                        fail_silently=False,
                        )

                    return Response({'response': 'HURRAYYY user and token have been created...sending back token', 'token': token.key})
            
                # if the username already exists
                except IntegrityError:
                    return Response({'response': 'username is taken'})
           
        except:
            return Response({'response': 'not all fields where provided...or something else went wrong'})
        


# reset password logic
class ResetPassword(APIView):
    
    def post(self,request):
        print('sdflgkgflkjl;lsdfjg;slzdfj')
        email = json.loads(request.body.decode('UTF-8'))['email']
        username = json.loads(request.body.decode('UTF-8'))['username']
        print(email, username)

        return Response({'response': 'email has been sent...maybe'})



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
          

# Find other users and request their friendship... this gets called after the the return button is pressed on the search bar
class FindFriends(APIView):
    
    # restrict access to authenticated users => they need to have token => they need to be logged in
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        search_term = json.loads(request.body)['search_term']

        # find the all the users with the search term in their username, exclude own user object
        results = User.objects.filter(username__contains=search_term).exclude(username=request.user)

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


# get all the messages for a certain conversation
class GetMessages(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_user = request.user
        friend = User.objects.get(username=json.loads(request.body.decode('UTF-8'))['friend'])
        
        # since a friendship can be sent or requested, check both cases

        try: 
            friendship = Friendship.objects.get(sender=current_user, receiver=friend)
            messages_from_db = Message.objects.filter(conversation=friendship)
            serializer = MessageSerializer(messages_from_db, many=True)
            return Response({'response': 'this is where the current user is the sender of the friendship.', 'messages': serializer.data, 'friendship_id': friendship.id})
        
        except:

            friendship = Friendship.objects.get(receiver=current_user, sender=friend)
            messages_from_db = Message.objects.filter(conversation=friendship)
            serializer = MessageSerializer(messages_from_db, many=True)
            return Response({'response': 'this is where the current user is the receiver of the friendship.', 'messages': serializer.data, 'friendship_id': friendship.id})



class RequestFriendship(APIView):

    # make sure the user is Authenticated
    permission_classed = (IsAuthenticated,)

    def post(self, request):

        # define the sender and the receiver user 
        current_user = request.user
        potentialFriend = User.objects.get(username=(json.loads(request.body.decode('UTF-8'))['potentialFriend']))
        
        # check if the friendship object already exists...this shouldn't be possible and if it is there's a bug somewhere
        first = Friendship.objects.filter(sender=current_user, receiver=potentialFriend)
        second = Friendship.objects.filter(sender=potentialFriend, receiver=current_user)

        if first.count != 0 or second.count != 0:
            return Response({'response': 'this friendship already exists'})

        # if the friendship doesn't exist create a new Friendship object
        elif first.count == 0 or second.count == 0:
            friendship = Friendship(sender=current_user, receiver=potentialFriend)
            friendship.save()
            return Response({'response': 'request sent'})


# logic to accept the friendship
class ConfirmFriendRequest(APIView):

    permission_classes = (IsAuthenticated,) 

    def post(self, request):

        # get the Friendship Obj based on the ID
        friendship = Friendship.objects.get(id=(json.loads(request.body.decode('UTF-8'))['friendshipId']))

       # make them friends, set a time for the friendship start and set the pending boolean to False
        friendship.are_they_friends = True
        now = datetime.datetime.now()
        friendship.date_confirmed = now
        friendship.pending = False
        friendship.save()

        # retrieve the updated info from the server..this includes info from the new friend
        newInfo = Get_info()
        return Response({'response': 'friendship confirmed', 'info': newInfo.info(request, 1)})


# logic that handles when if the user ignores the friend request
class IgnoreFriendship(APIView):
    
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # get the friendship through the id
        friendship = Friendship.objects.get(id=(json.loads(request.body.decode('UTF-8'))['friendshipId']))
        
        # set the pending to False and Rejected to true, set a date for when this happened
        friendship.pending = False
        friendship.rejected = True
        now = datetime.datetime.now()
        friendship.date_confirmed = now
        friendship.save()
        
        return Response({'response': 'request ignored'})


#logic to unfriend current friends
class Unfriend(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        soonExFriend = User.objects.get(username=(json.loads(request.body.decode('UTF-8'))['soonExFriend']))


        # find the friendship it can be sent or received
        sentFriendship = Friendship.objects.filter(sender=request.user, receiver=soonExFriend, pending=False)
        receivedFriendship = Friendship.objects.filter(sender=soonExFriend, receiver=request.user, pending=False)

        try:
            to_delete = sentFriendship[0]
            to_delete.delete()

            newInfo = Get_info()

            return Response({'response': 'friendship was deleted', 'info': newInfo.info(request, 1)})

        except:
            to_delete = receivedFriendship[0]
            to_delete.delete()

            newInfo = Get_info()

            return Response({'response': 'friendship was deleted...received Friendship', 'info': newInfo.info(request, 1)})
        
        

