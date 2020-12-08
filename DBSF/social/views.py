from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'social/index.html', {'user': request.user})
    else:
        return render(request, 'social/login.html')


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

            if username == '' or first =='' or last == '' or email == '' or dob == '':
                return render(request, 'social/login.html', {'message': 'You must provide all the fields'})

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'social/index.html', {'message': 'You have been logged in', 'user': request.user})

        else:
            return render(request, 'social/login.html', {'message': "Invalid login credentials"})

    elif request.method == 'GET':
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'social/login.html', {'message':'You have been logged out'})

    else:
        return render(request, 'social/index.html', {'message': 'you must log out via the logout button'})
