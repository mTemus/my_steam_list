from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users_library.models import Collection, UserAppData

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer):
        model = User
        fields = ('id', 'email', 'username', 'password')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["name"]
        
class UserAppDataCreateSerializer(serializers.ModelSerializer):
    app_data = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    collections = CollectionSerializer(read_only=True, many=True)
    
    class Meta:
        model = UserAppData
        fields = [
                "app_data", 
                "status", 
                "score", 
                "collections", 
                "start_date", 
                "end_date", 
                "hours_spent"] 

class UserAppDataUpdateSerializer(serializers.ModelSerializer):
    app_data = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    collections = CollectionSerializer(read_only=True, many=True)
    
    class Meta:
        model = UserAppData
        fields = [
                "id",
                "status", 
                "score", 
                "collections", 
                "start_date", 
                "end_date", 
                "hours_spent"]

class UserAppDataSerializer(serializers.ModelSerializer):
    app_data = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    collections = CollectionSerializer(read_only=True, many=True)
    
    class Meta:
        model = UserAppData
        fields = [
                "id",
                "name",
                "user",
                "app_data", 
                "status", 
                "score", 
                "collections", 
                "start_date", 
                "end_date", 
                "hours_spent"] 