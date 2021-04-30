from rest_framework import serializers
from social.models import User, Comment

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'profile_pic']


class CommentSerializer(serializers.ModelSerializer):

  commentator = serializers.ReadOnlyField(source='commentator.username')

  class Meta:
    model = Comment
    fields = ['id', 'post', 'commentator', 'text', 'date', 'likes']
