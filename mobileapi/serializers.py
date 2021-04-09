from rest_framework import serializers
from social.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'profile_pic']