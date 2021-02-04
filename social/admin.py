from django.contrib import admin
from .models import User, Post, Friendship, Message, Comment, Like, Dislike


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)