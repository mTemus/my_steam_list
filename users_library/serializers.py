from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from games_library.models import AppData

from users_library.models import Collection

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer):
        model = User
        fields = ('id', 'email', 'username', 'password')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["name"]
        
class UserAppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppData
        fields = ["app_data", 
                "status", 
                "score", 
                "collections", 
                "start_date", 
                "end_date", 
                "hours_spent"] 
