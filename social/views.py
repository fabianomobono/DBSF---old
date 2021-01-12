from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Post, Friendship, Message
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
import datetime
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'requests': Friendship.objects.filter(receiver=request.user, pending=True),
            'posts': Post.objects.all().order_by("-date")}
        return render(request, 'social/index.html', context)
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first = form.cleaned_data['First_name']
            last = form.cleaned_data['Last_name']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['password_confirmation']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']

            if username == '1' or first == '' or last == '' or email == '' or dob == '':
                return render(request, 'social/login.html', {'message': 'You must provide all the fields', 'form': LoginForm(), 'register_form': form})

            if password != confirmation:
                return render(request, 'social/login.html', {'message': 'Password and confirmationdo not match'})

            else:
                try:
                    user = User.objects.create_user(username=username, first_name=first, last_name=last, email=email, password=password, dob=dob)

                except IntegrityError:
                    return render(request, 'social/login.html', {'message': 'Username is taken'})

                login(request, user)
                return HttpResponseRedirect(reverse('index'))

        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('form is valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return render(request, 'social/login.html', {'message': "Invalid login credentials", 'form': form, 'register_form': RegisterForm()})

        else:
            return render(request, 'social/login.html', {'message': "You have to provide all the fields", 'form': form, 'register_form': RegisterForm()})

    elif request.method == 'GET':
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'social/profile.html', {'user': request.user, 'posts': posts})


@login_required
@require_http_methods(['POST'])
def change_profile_pic(request):
    picture = request.FILES['profile_pic']
    print(picture)
    user = User.objects.get(username=request.user)
    user.profile_pic = picture
    user.save()
    return HttpResponseRedirect(reverse('profile'))


@login_required
@require_http_methods(['POST'])
def create_new_post(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    text = data['text']
    new_post = Post(author=request.user, text=text)
    new_post.save() 
    response = {'author': new_post.author.username, 'date': new_post.date, 'id': new_post.id, 'text': text}
    return JsonResponse(response)


# delete post 
@login_required
@require_http_methods(['POST'])
def delete_post_function(request):
    
    data = json.loads(request.body.decode("utf-8"))
    print(data['post_author'])
    print(request.user)
    if str(data['post_author']) == str(request.user):
        post_to_delete = Post.objects.get(id=data['id'])
        post_to_delete.delete()
        response = {'response': "post was deleted"}
        return JsonResponse(response)
    else:
        response = {'response': 'you can only delete your own posts'}
        return JsonResponse(response)


@login_required
@require_http_methods(['GET'])
def friends_profile(request, friend):
    friend_user = User.objects.get(username=friend)
    posts = Post.objects.filter(author=(User.objects.get(username=friend)))
    friendship_requested = Friendship.objects.filter(sender=request.user, receiver=friend_user)
    friendship_sent = Friendship.objects.filter(sender=friend_user)
    friendship_status = {'status': 'False'}
    

    # check the friendship status between the two users
    print('requested: ', friendship_requested.count())
    print('sent: ', friendship_sent.count())
    if friendship_requested.count() != 0:
        if friendship_requested[0].pending == True:            
            friendship_status['status'] = 'Pending'
        else:
            friendship_status['status'] = 'Friends'

    elif friendship_sent.count() != 0:
        if friendship_sent[0].pending == True:  
            friendship_status['status'] = 'Pending'
        else:
            friendship_status['status'] = 'Friends'


    return render(request, 'social/friends_profile.html', {'user': request.user, 'friend': friend_user, 'posts': posts, 'status': friendship_status['status'] })



def get_posts(request):
    response = {'response': [], 'username': request.user.username, 'profile_pic': request.user.profile_pic.url}
    posts = Post.objects.all().order_by('-date')
    for post in posts:
        response['response'].append({'id': post.id, 'author': post.author.username, 'text': post.text, 'date': post.date, 'author_picture': post.author.profile_pic.url})   
    return JsonResponse(response)
    

def request_friendship(request):
    # get the firend user  
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


def get_friend_requests(request):
    requests = Friendship.objects.filter(receiver=request.user, pending=True)
    response  = {'requests': [] }
    for request in requests:
        response['requests'].append({'sender': request.sender.username, 'sender_profile_pic': request.sender.profile_pic.url, 'id': request.id})
    return JsonResponse(response)


# confirm friend request
def confirm_friend_request(request):
    friendship = Friendship.objects.get(id=(request.body.decode('ascii')))
    friendship.are_they_friends = True
    now = datetime.datetime.now()
    friendship.date_confirmed = now
    friendship.pending = False
    friendship.save()
    response = {'response': 'friendship confirmed'}
    return JsonResponse(response)


def ignore_friend_request(request):
    friendship = Friendship.objects.get(id=(request.body.decode('ascii')))
    friendship.pending = False
    friendship.rejected = True
    now = datetime.datetime.now()
    friendship.date_confirmed = now
    friendship.save()
    response = {'response': 'request ignored'}
    print(friendship)
    return JsonResponse(response)


def get_friends(request):
    friends_received = Friendship.objects.filter(receiver=request.user, pending=False)
    friends_sent = Friendship.objects.filter(sender=request.user, pending=False)    
    friends = []
    for f in friends_received:
        friends.append({'user': f.sender.username, 'profile_pic': f.sender.profile_pic.url, 'id': f.id})
    
    for s in friends_sent:
        friends.append({'user': s.receiver.username, 'profile_pic':s.receiver.profile_pic.url, 'id': s.id})

    response = {'response': friends, 'user': request.user.username}
    return JsonResponse(response)


def get_friendship_id(request):
    data = json.loads(request.body.decode('utf-8'))
    sender = data['sender']
    receiver = data['receiver']
    
    try: 
        friendship = Friendship.objects.get(sender=(User.objects.get(username=sender)),receiver=(User.objects.get(username=receiver)))
        messages_from_db = Message.objects.filter(conversation=friendship)
        
        messages = []
        for message in messages_from_db:
            messages.append({'sender': message.sender.username, 'receiver': message.receiver.username, 'text': message.text, 'date_sent': message.date_sent})
        
        response = {'id': friendship.id, 'messages': messages}
        return JsonResponse(response)
    
    except:
        friendship = Friendship.objects.get(sender=(User.objects.get(username=receiver)),receiver=(User.objects.get(username=sender)))
        messages_from_db = Message.objects.filter(conversation=friendship)
        
        messages = []
        for message in messages_from_db:
            messages.append({'sender': message.sender.username, 'receiver': message.receiver.username, 'text': message.text, 'date_sent': message.date_sent})
        
        response = {'id': friendship.id, 'messages': messages}
        return JsonResponse(response)


@require_http_methods(['GET'])
@login_required
def find_friends(request):
    search_term = str(request.GET['search_term'])
    results = User.objects.filter(username__contains=search_term)
    users = []
    for user in results:
        # check if current user and user are friends
        requested = Friendship.objects.filter(sender=request.user, receiver=user)
        received = Friendship.objects.filter(sender=user, receiver=request.user)

        # if a Friendship object exists
        if requested.count() != 0:
            # check if it is pending
            if requested[0].pending == True:
                users.append({'user': user, 'status': 'Pending', 'profile_pic': user.profile_pic.url})
            else:
                users.append({'user': user, 'status': 'Friends', 'profile_pic': user.profile_pic.url})

        elif received.count() != 0:
            # check if it is pending
            if received[0].pending == True:
                users.append({'user': user, 'status': 'Pending', 'profile_pic': user.profile_pic.url})
            else:
                users.append({'user': user, 'status': 'Friends', 'profile_pic': user.profile_pic.url})

        else:
            users.append({'user': user, 'status': "not friends", 'profile_pic': user.profile_pic.url})


    
    return render(request, 'social/find_friends.html', {'users': users})