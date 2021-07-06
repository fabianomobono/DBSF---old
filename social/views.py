from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Post, Friendship, Message, Comment, Like, Dislike, Get_info, Get_one_persons_posts
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
import datetime
from django.views import View
import arrow
from social_django.utils import psa
from google.oauth2 import id_token
from google.auth.transport import requests

# Create your views here.
class Index(View):
    # if it is a get request
    def get(self, request):
        if request.user.is_authenticated:        
            return render(request, 'social/sandbox.html')
        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


class RegisterView(View):
    
    # if it is a post request
    def post(self, request, *args, **kwargs):     
        form = RegisterForm(request.POST)
        if form.is_valid():

            # get data from the form
            username = form.cleaned_data['username']
            first = form.cleaned_data['First_name']
            last = form.cleaned_data['Last_name']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['password_confirmation']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']

            # check if all the fieds are provided
            if username == '1' or first == '' or last == '' or email == '' or dob == '':
                return render(request, 'social/login.html', {'message': 'You must provide all the fields', 'form': LoginForm(), 'register_form': form})

            # if the password and the confirmation do not match
            if password != confirmation:
                return render(request, 'social/login.html', {'message': 'Password and confirmationdo not match', 'form': LoginForm(), 'register_form': form})

            # if they match try to create a user 
            else:
                try:
                    user = User.objects.create_user(username=username, first_name=first, last_name=last, email=email, password=password, dob=dob)

                # if a user with that username already exists 
                except IntegrityError:
                    return render(request, 'social/login.html', {'message': 'Username is taken', 'form': LoginForm(), 'register_form': form})

                # if everything goes well log the user in and redirect to the main page
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

        # if the form is not valid
        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


class LoginView(View):

    # if it id a post request
    def post(self, request, *args, **kwargs):        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # if the authentication process succeeds
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            # if not notify "invalid login credentials"
            else:
                return render(request, 'social/login.html', {'message': "Invalid login credentials", 'form': form, 'register_form': RegisterForm()})

        # if the form is not valid
        else:
            return render(request, 'social/login.html', {'message': "You have to provide all the fields", 'form': form, 'register_form': RegisterForm()})

    # if it is a get request show the login page
    def get(self, request):
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


# this logs the user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# this shows the userpage in the multi page app => this is from the old version of the app and can be deleted
@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):      
        posts = Post.objects.filter(author=request.user).order_by('-date')
        return render(request, 'social/profile.html', {'user': request.user, 'posts': posts})



# changes or upload profile_pic
@login_required
@require_http_methods(['POST'])
def change_profile_pic(request):

    # retrieve the pic from the request and save it
    picture = request.FILES['profile_pic']   
    user = User.objects.get(username=request.user)
    user.profile_pic = picture
    user.save()
    return JsonResponse({'profile_pic': user.profile_pic.url})


# this contains the logic to create a new post
@method_decorator(login_required, name='dispatch')
class Create_new_post(View):
    def post(self, request):

        # get all the nevessary data from the POST request and save the post
        data = json.loads(request.body.decode("utf-8"))        
        text = data['text']
        new_post = Post(author=request.user, text=text)  
        new_post.save()
        
        # get the current time from the arrow library and humanize the time display
        time_arrow = arrow.utcnow() 
        response = {
            'author': new_post.author.username, 
            'date': time_arrow.humanize(), 
            'id': new_post.id, 
            'text': text,
            'comments': []}
        return JsonResponse(response)


# delete post from database here 
@login_required
@require_http_methods(['POST'])
def delete_post_function(request):

    # get the information necessary to delete the post    
    data = json.loads(request.body.decode("utf-8"))

    # make double check if the author of the post and the person deleting the post is the same user
    if str(data['post_author']) == str(request.user):

        # if so delete the post
        post_to_delete = Post.objects.get(id=data['id'])
        post_to_delete.delete()
        response = {'response': "post was deleted"}
        return JsonResponse(response)
    else:
        response = {'response': 'you can only delete your own posts'}
        return JsonResponse(response)


# render the friends profile. This is from the old (multipage-app) version and can be deleted 
@login_required
@require_http_methods(['GET'])
def friends_profile(request, friend):

    # get the friend user
    friend_user = User.objects.get(username=friend)

    # get all the users posts 
    posts = Post.objects.filter(author=(User.objects.get(username=friend)))
    friendship_requested = Friendship.objects.filter(sender=request.user, receiver=friend_user)
    friendship_sent = Friendship.objects.filter(sender=friend_user, receiver=request.user)
    friendship_status = {'status': 'False'}
    
    # check the friendship status between the two users for button

    if friendship_requested.count() != 0:
        if friendship_requested[0].pending == True:            
            friendship_status['status'] = 'Pending'
        else:
            if friendship_requested[0].rejected == True:
                friendship_status['status'] = 'Rejected'
            else: 
                friendship_status['status'] = 'Friends'

    elif friendship_sent.count() != 0:
        if friendship_sent[0].pending == True:  
            friendship_status['status'] = 'Pending'
        else:
            if friendship_sent[0].rejected == True:
                friendship_status['status'] = 'Rejected'
            else:
                friendship_status['status'] = 'Friends'

    return render(request, 'social/friends_profile.html', {'posts': posts, 'user': request.user, 'friend': friend_user, 'status': friendship_status['status']})

       
# this gets called when the user clicks on the Home button, the request starts from sandbox.js in the App component in the 'main' method
def get_posts(request):
    page_number = 1
    info = Get_info()
    response = info.info(request, page_number)['posts']
    return JsonResponse({'response': response})
    

# request friendship    
@login_required
def request_friendship(request):
    # get the friend user  
    receiver = User.objects.get(username=(request.body.decode('ascii')))

    # check if this Friendship (or it's opposite already exists)
    first = Friendship.objects.filter(sender=request.user, receiver=receiver)
    second = Friendship.objects.filter(receiver=request.user, sender=receiver)
    if first.count() != 0 or second.count() != 0:
         response = {'response': "this Friendship already exists"}
         return JsonResponse(response)
    
    # create the frienship 
    else:
        friendship = Friendship(sender=request.user, receiver=receiver)
        friendship.save()
        response = {'response': 'Friendship requested'}
        return JsonResponse(response)


# get all the pending friendship request that a user has
def get_friend_requests(request):
    requests = Friendship.objects.filter(receiver=request.user, pending=True)
    response  = {'requests': [] }
    for request in requests:
        response['requests'].append({'sender': request.sender.username, 'sender_profile_pic': request.sender.profile_pic.url, 'id': request.id})
    return JsonResponse(response)


# confirm friend request
def confirm_friend_request(request):

    # get the friendship object based on the id from the request
    friendship = Friendship.objects.get(id=(request.body.decode('ascii')))

    # make them friends, set a time for the friendship start and set the pending boolean to False
    friendship.are_they_friends = True
    now = datetime.datetime.now()
    friendship.date_confirmed = now
    friendship.pending = False
    friendship.save()

    # reload posts and friends with the new friends posts
    a = Get_info()
    response = {'response': 'friendship confirmed', 'updated_info': a.info(request, 1)}
    
    return JsonResponse(response)


# ignore a friend request made to the user 
def ignore_friend_request(request):

    # get the correct object of the request
    friendship = Friendship.objects.get(id=(request.body.decode('ascii')))

    # set the pending to False and Rejected to true
    friendship.pending = False
    friendship.rejected = True
    now = datetime.datetime.now()
    friendship.date_confirmed = now
    friendship.save()
    response = {'response': 'request ignored'}
    
    return JsonResponse(response)



# forgot password logic
def set_new_password(request):
    return render(request, 'social/set_new_password.html')

def forgot_password(request):
    return render(request, 'social/forgot_password.html')



#delete friendship
@login_required
@require_http_methods(['POST'])
def unfriend(request):

    # find the friendship, it could be have been sent or received
    user = request.body.decode('utf-8')
    sent_friendships = Friendship.objects.filter(sender=(User.objects.get(username=user)), receiver=request.user, pending=False)
    received_friendships = Friendship.objects.filter(sender=request.user, receiver=(User.objects.get(username=user)), pending=False)
    
    # depending on which it was delete the correct object
    try:
        to_delete = sent_friendships[0]
        to_delete.delete()
        response = {'response': 'unfriended_sent'}
        return JsonResponse(response)
    except:
        to_delete = received_friendships[0]
        to_delete.delete()
        response = {'response': 'unfriended_received'}
        return JsonResponse(response)


# this is necessary for the direct messaging feature. The Friendship ID will be used to create a Websocket 
def get_friendship_id(request):

    # get all the necessary data from the request
    data = json.loads(request.body.decode('utf-8'))
    sender = data['sender']
    receiver = data['receiver']
    
    # since the friendship can be requested or sent, check both cases
    try: 
        friendship = Friendship.objects.get(sender=(User.objects.get(username=sender)),receiver=(User.objects.get(username=receiver)))
        messages_from_db = Message.objects.filter(conversation=friendship)
        
        messages = []
        for message in messages_from_db:
            messages.append({'sender': message.sender.username, 'receiver': message.receiver.username, 'text': message.text, 'date_sent': message.date_sent, 'id': message.id})
        
        response = {'id': friendship.id, 'messages': messages}
        return JsonResponse(response)
    
    except:
        friendship = Friendship.objects.get(sender=(User.objects.get(username=receiver)),receiver=(User.objects.get(username=sender)))
        messages_from_db = Message.objects.filter(conversation=friendship)
        
        messages = []
        for message in messages_from_db:
            messages.append({'sender': message.sender.username, 'receiver': message.receiver.username, 'text': message.text, 'date_sent': message.date_sent, 'id': message.id})
        
        response = {'id': friendship.id, 'messages': messages}
        return JsonResponse(response)


# this gets triggered if the user looks for friends in the main search box
@require_http_methods(['GET'])
@login_required
def find_friendss(request):
    # get all the users that contain the seatch term in the username
    search_term = str(request.GET['search_term'])
    results = User.objects.filter(username__contains=search_term).exclude(username=request.user)
    users = []

    # for each user in that the database spits out
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

    return JsonResponse({'users': users})

# this gets called when the user clicks on it's own profaile page
def get_own_posts(request):
    # get all the users's posts
    posts = Get_one_persons_posts()

    # get the page number for the paginator
    page_number = int(request.GET['page_number'])
    
    # actually get the posts
    answer = posts.posts(request.user, request, page_number)['posts']
    response = {'response': answer}
    return JsonResponse(response)
    

# save comments to a post
class Comment_a_post(View):

    def post(self, request):

        # get the data from the post request
        data = json.loads(request.body.decode("utf-8"))
        post = Post.objects.get(pk=data["post_id"])
        text = str(data["text"])
        commentator = request.user

        # save the comment
        comment = Comment(post=post, commentator=commentator, text=text)
        comment.save()
        response = {
            "id": comment.id, 
            "text": comment.text, 
            "commentator": comment.commentator.username, 
            "profile_pic": request.user.profile_pic.url, 
            "date": comment.date,
            "likes": comment.likes}
        return JsonResponse(response)

    # this actually doesn't do anything..it's just a little code snippet to test future REST frameworks
    def get(self, request):
        response = {'response': 'this worked'}
        return JsonResponse(response)


class Like_a_post(View):
    def post(self, request):

        # get the data from the request
        post_id = json.loads(request.body.decode('utf-8'))['post_id']
        post = Post.objects.get(pk=post_id)
        try:
            # if the post has already been liked 
            already_liked = Like.objects.get(post=post, user=request.user)
            response = {'response': 'you already liked this post'}
            return JsonResponse(response)
        except:
            # if not create the like
            like = Like(user=request.user, post=post)
            like.save()
            response = {'response': 'like created'}
            return JsonResponse(response)

# same as like a post
class Dislike_a_post(View):
    def post(self,request):
        post_id = json.loads(request.body.decode('utf-8'))['post_id']
        post = Post.objects.get(pk=post_id)
        try: 
            already_disliked = Dislike.objects.get(post=post, user=request.user)
            response = {'response': 'you already disliked this post'}
            return JsonResponse(response)
        except:
            dislike = Dislike(user=request.user, post=post)
            dislike.save()
            response = {'response': 'dislike created'}
            return JsonResponse(response)


# logic for the single page app update
@method_decorator(login_required, name='dispatch')
class Sandbox(View):

    # get request when tha main page gets loaded
    def get(self, request):
        print(request.body)
        return render( request, 'social/sandbox.html')
    
    # get all the necessary data to display the main page
    def post(self, request):      
        page_number = json.loads(request.body.decode('utf-8'))['page_number']
        info = Get_info()
        response = info.info(request, page_number)
        return JsonResponse(response)


class Friends_profile_sandbox(View):

    def post(self, request):
        # get the friend from the request body
        friend = json.loads(request.body.decode('utf-8'))['friend']
        page_number = json.loads(request.body.decode('utf-8'))['page_number']
        posts = Get_one_persons_posts()

        # get the data necessary to display a friends profile
        answer = posts.posts(friend, request, page_number)
        print('Yup this worked so well just like that')
        return JsonResponse(answer)


def play(request):
  return render(request, 'social/play.html')


@psa()
def google_log_in(request, backend):
    auth_token = json.loads(request.body.decode('utf-8'))['auth_token']
    print(auth_token)
    c = '353768358220-h0erg8v47qp5sa12ikvf3pluejlis03s.apps.googleusercontent.com'
    idinfo = id_token.verify_oauth2_token(auth_token, requests.Request(), c)
    print(auth_token, '24234234')
    print(idinfo)
    user = request.backend.do_auth(idinfo)
    print(user)
    return JsonResponse(idinfo)