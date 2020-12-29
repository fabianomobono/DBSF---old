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


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.author} posted: {self.text}'


class Friendship(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requesting_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirming_user")
    pending = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)
    are_they_friends = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(blank=True, null=True)
   
    def __str__(self):
        if self.are_they_friends:
            return f'Are {self.sender} and {self.receiver} friends? Yes' 
        else:
            return f'Are {self.sender} and {self.receiver} friends? No' 