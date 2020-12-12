from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone
from django.utils.html import mark_safe
# Create your models here.


class User(AbstractUser):
    dob = models.DateField(blank=True, default=timezone.now)
    friends = models.IntegerField(default=0)
    profile_pic = models.ImageField(blank=True, upload_to='profile_pictures')
