from django.db.models import fields
from rest_framework import serializers
from users.models import User

class UserCreateSerializer(serializers.Serializer):
    
    class Meta:
        model = User
        fields = "__all__"
