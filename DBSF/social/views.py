from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Post
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        print(Post.objects.all())
        return render(request, 'social/index.html', {'user': request.user, 'posts': Post.objects.all().order_by("-date")})
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
    return render(request, 'social/profile.html', {'user': request.user})


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
    new_post = Post(author=request.user, text=data['text'])
    new_post.save()
    data['date']= new_post.date
    return JsonResponse(data)


@login_required
@require_http_methods(['GET'])
def friends_profile(request):
    return render(request, 'social/friends_profile.html')