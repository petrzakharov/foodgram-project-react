from django.db.models import fields
from rest_framework import serializers
from users.models import User
from djoser.serializers import UserCreateSerializer


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('first_name','last_name','username','email','password')
