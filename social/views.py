from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Post, Friendship, Message, Comment, Like, Dislike
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


# Create your views here.
class Index(View):

    def get(self, request):
        if request.user.is_authenticated:        
            return render(request, 'social/index.html')
        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


class RegisterView(View):
    
    # if it is a post request
    def post(self, request, *args, **kwargs):     
        form = RegisterForm(request.POST)
        if form.is_valid():
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

            if password != confirmation:
                return render(request, 'social/login.html', {'message': 'Password and confirmationdo not match', 'form': LoginForm(), 'register_form': form})

            else:
                try:
                    user = User.objects.create_user(username=username, first_name=first, last_name=last, email=email, password=password, dob=dob)

                except IntegrityError:
                    return render(request, 'social/login.html', {'message': 'Username is taken', 'form': LoginForm(), 'register_form': form})

                # if everything goes well log the user in and redirect to the main page
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

        # if the form is no valid
        else:
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


class LoginView(View):
    def post(self, request, *args, **kwargs):        
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

    def get(self, request):
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):      
        posts = Post.objects.filter(author=request.user).order_by('-date')
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


@method_decorator(login_required, name='dispatch')
class Create_new_post(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        text = data['text']
        new_post = Post(author=request.user, text=text)  
        new_post.save()
        time_arrow = arrow.utcnow() 
        response = {
            'author': new_post.author.username, 
            'date': time_arrow.humanize(), 
            'id': new_post.id, 
            'text': text,
            'comments': []}
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


class Friends_posts(View):
    def post(self, request):
        friend = User.objects.get(username=request.body.decode('ascii'))
        posts = Post.objects.filter(author=(friend))
        response = {'response': [], 'username': request.user.username, 'profile_pic': friend.profile_pic.url}

        # get all the posts from that user and store it in the response dict
        for post in posts:

            # get all the comments for each post
            comments = Comment.objects.filter(post=post)
            c = []
            for comment in comments:
                c.append({
                    'commentator': comment.commentator.username, 
                    'profile_pic': comment.commentator.profile_pic.url, 
                    'text': comment.text, 
                    'date':comment.date, 
                    'likes': comment.likes,
                    'id': comment.id})
            
            # sort the comments by date
            c.sort(key = lambda x:x['date'])
            
            
            # hmanize the date for each comment
            for comment in c:
                comment['date'] = arrow.get(comment['date']).humanize()

            # get all the likes for this post
            l = Like.objects.filter(post=post)
            likes = []
            for like in l:
                likes.append({
                    'post_id': like.post.id,
                    'user': like.user.username,
                    'profile_pic': like.user.profile_pic.url
                })

            # get all the dislikes for this post
            d = Dislike.objects.filter(post=post)
            dislikes = []
            for dislike in d: 
                dislikes.append({
                    'post_id': dislike.post.id,
                    'user': like.user.username,
                    'profile_pic': like.user.profile_pic.url
                })

            response['response'].append({
                'id': post.id, 
                'author': post.author.username, 
                'text': post.text, 
                'date': post.date.strftime("%a %b %d, at %I:%M %p"),
                'author_picture': friend.profile_pic.url,
                'likes': likes,
                'dislikes': dislikes,
                'comments': c
                })

        response['response'].sort(key = lambda x:x['date'])
        response['response'].reverse()
        return JsonResponse(response)
        

def get_posts(request):
    # prepare response
    response = {'response': [], 'username': request.user.username, 'profile_pic': request.user.profile_pic.url}
    
    # get friends
    sent = Friendship.objects.filter(sender=request.user, pending=False, rejected=False)
    received = Friendship.objects.filter(receiver=request.user, pending=False, rejected=False)
    
    posts = []

    # get your own posts
    own_posts = Post.objects.filter(author=request.user)
    for o in own_posts:
        # if it is a post and not an empty Queryset
        if type(o) == Post:
            posts.append(o)

    # get posts from friendships you've sent
    for s in sent:
        post = Post.objects.filter(author=s.receiver)

        # if the QuerySet is not empty
        if len(post) != 0:
            for p in post:
                posts.append(p)

    # get posts from  friendships you've received
    for r in received:
        post = Post.objects.filter(author=r.sender)

        # if the queryset is not empty
        if len(post) != 0:
            for p in post:
                posts.append(p)
    
    for post in posts:
        # get the comments
        comments = Comment.objects.filter(post=post)
        c = []

        # for each comment
        for comment in comments:
            c.append({
            'commentator': comment.commentator.username,
            'profile_pic': comment.commentator.profile_pic.url, 
            'text': comment.text, 
            'date':comment.date, 
            'likes': comment.likes,
            'id': comment.id})
           
        # sort the comments by date
        c.sort(key = lambda x:x['date'])
            
        # humanize the date for each comment
        for comment in c:
            comment['date'] = arrow.get(comment['date']).humanize()
        

        # get all the likes for this post
        l = Like.objects.filter(post=post)
        likes = []
        for like in l:
            likes.append({
                'post_id': like.post.id,
                'user': like.user.username,
                'profile_pic': like.user.profile_pic.url
            })

        # get all the dislikes for this post
        d = Dislike.objects.filter(post=post)
        dislikes = []
        for dislike in d: 
            dislikes.append({
                'post_id': dislike.post.id,
                'user': dislike.user.username,
                'profile_pic': dislike.user.profile_pic.url
            })
        
        # store all the data necessary for the post in response['response']
        response['response'].append({
            'id': post.id, 
            'author': post.author.username, 
            'text': post.text, 
            'date': post.date, 
            'author_picture': post.author.profile_pic.url,
            'comments': c,
            'likes': likes,
            'dislikes': dislikes,
            }) 
    
    # sort by -date
    response['response'].sort(key = lambda x:x['date'])
    response['response'].reverse()
    
    #humanize the date for each post
    for post in response['response']:
        post['date'] = arrow.get(post['date']).humanize()

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


#delete friendship
@login_required
@require_http_methods(['POST'])
def unfriend(request):
    user = request.body.decode('utf-8')
    sent_friendships = Friendship.objects.filter(sender=(User.objects.get(username=user)), receiver=request.user, pending=False)
    received_friendships = Friendship.objects.filter(sender=request.user, receiver=(User.objects.get(username=user)), pending=False)
    try:
        to_delete = sent_friendships[0]
        to_delete.delete()
        response = {'response': 'unfirended_sent'}
        return JsonResponse(response)
    except:
        to_delete = received_friendships[0]
        to_delete.delete()
        response = {'response': 'unfriended_received'}
        return JsonResponse(response)


def get_friends(request):
    # get all of the user's friends. Received and sent Friendships
    friends_received = Friendship.objects.filter(receiver=request.user, pending=False, rejected=False)
    friends_sent = Friendship.objects.filter(sender=request.user, pending=False, rejected=False)    
    friends = []
    for f in friends_received:
        friends.append({'user': f.sender.username, 'profile_pic': f.sender.profile_pic.url, 'id': f.id})
    
    for s in friends_sent:
        friends.append({'user': s.receiver.username, 'profile_pic':s.receiver.profile_pic.url, 'id': s.id})

    # get the last message (if it exists) that was sent to each friend
    for f in friends:
        friendship = Friendship.objects.get(id=f['id']) 
        message = Message.objects.filter(conversation=friendship).order_by('-date_sent')
        if len(message) != 0:
            print(f)
            f['last_message_date'] = message[0].date_sent.strftime("%a %b %d, %Y %H:%M:%S")
        else:
            f['last_message_date'] = 'No message was sent yet'
        print('added: ', f)
       
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
                users.append({'user': user, 'status': 'Pending', 'profile_pic': user.profile_pic.url, 'rejected': False})
            else:
                users.append({'user': user, 'status': 'Friends', 'profile_pic': user.profile_pic.url, 'rejected': requested[0].rejected})

        elif received.count() != 0:
            # check if it is pending
            if received[0].pending == True:
                users.append({'user': user, 'status': 'Pending', 'profile_pic': user.profile_pic.url , 'rejected': False})
            else:
                users.append({'user': user, 'status': 'Friends', 'profile_pic': user.profile_pic.url, 'rejected': received[0].rejected})

        else:
            users.append({'user': user, 'status': "not friends", 'profile_pic': user.profile_pic.url})


    
    return render(request, 'social/find_friends.html', {'users': users})


def get_own_posts(request):
    # get all the users's posts
    posts = Post.objects.filter(author=request.user)
    response = {'response': [], 'username': request.user.username, 'profile_pic': request.user.profile_pic.url}

    
    for post in posts:

        # get all the comments for each post
        comments = Comment.objects.filter(post=post)
        c = []
        for comment in comments:
            c.append({
                'commentator': comment.commentator.username, 
                'profile_pic': comment.commentator.profile_pic.url, 
                'text': comment.text, 
                'date':comment.date, 
                'likes': comment.likes,
                'id': comment.id})
        
        # sort the comments by date
        c.sort(key = lambda x:x['date'])
        
        
        # hmanize the date for each comment
        for comment in c:
            comment['date'] = arrow.get(comment['date']).humanize()

        
        # get all the likes for this post
        l = Like.objects.filter(post=post)
        likes = []
        for like in l:
            likes.append({
                'post_id': like.post.id,
                'user': like.user.username,
                'profile_pic': like.user.profile_pic.url
            })

        # get all the dislikes for this post
        d = Dislike.objects.filter(post=post)
        dislikes = []
        for dislike in d: 
            dislikes.append({
                'post_id': dislike.post.id,
                'user': like.user.username,
                'profile_pic': like.user.profile_pic.url
            })

        response['response'].append({
            'id': post.id, 
            'author': post.author.username, 
            'text': post.text, 
            'date':post.date.strftime("%a %b %d, at %I:%M %p"),
            'author_picture': request.user.profile_pic.url,
            'likes': likes,
            'dislikes': dislikes,
            'comments': c
            })

    # order posts -date
    response['response'].sort(key = lambda x:x['date'])
    response['response'].reverse()
    return JsonResponse(response)


# save comments to a post
class Comment_a_post(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        post = Post.objects.get(pk=data['post_id'])
        text = str(data['text'])
        commentator = request.user
        comment = Comment(post=post, commentator=commentator, text=text)
        comment.save()
        response = {
            'id': comment.id, 
            'text': comment.text, 
            'commentator': comment.commentator.username, 
            'profile_pic': request.user.profile_pic.url, 
            'date': comment.date,
            'likes': comment.likes}
        return JsonResponse(response)


class Like_a_post(View):
    def post(self, request):
        post_id = json.loads(request.body.decode('utf-8'))['post_id']
        post = Post.objects.get(pk=post_id)
        try: 
            already_liked = Like.objects.get(post=post, user=request.user)
            response = {'response': 'you already liked this post'}
            return JsonResponse(response)
        except:
            like = Like(user=request.user, post=post)
            like.save()
            response = {'response': 'like created'}
            return JsonResponse(response)


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


@method_decorator(login_required, name='dispatch')
class Sandbox(View):

    def get(self, request): 
        manager = Friendship.buddies.are_they_friends()      
        return render(request, 'social/sandbox.html', {'manager': manager})