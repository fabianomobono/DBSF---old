from django.shortcuts import render
from .forms import LoginForm, RegisterForm
# Create your views here.
def login(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'social/login.html' , {'form': login_form, 'register_form': register_form})
