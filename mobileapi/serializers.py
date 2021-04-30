from rest_framework import serializers
from social.models import User, Comment

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'profile_pic']


class CommentSerializer(serializers.ModelSerializer):

  commentator = serializers.ReadOnlyField(source='commentator.username')
  profile_pic = serializers.ReadOnlyField(source='commentator.profile_pic.url')
  class Meta:
    model = Comment
    fields = ['id', 'post', 'commentator', 'profile_pic', 'text', 'date', 'likes']
