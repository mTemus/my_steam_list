from rest_framework import serializers
from games_library.models import AppEntityData, Category, Collection, Entity, Genre, ImageData, Release

class AppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppEntityData
        fields = ["app_id", 
                "name", 
                "type", 
                "parent_app", 
                "dlc", 
                "short_desc", 
                "full_desc", 
                "about", 
                "images", 
                "developers", 
                "publishers", 
                "genres", 
                "categories", 
                "release"]

class UserAppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppEntityData
        fields = ["app_data", 
                "status", 
                "score", 
                "collections", 
                "start_date", 
                "end_date", 
                "hours_spent"] 

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["name"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["name"]

class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = ["header", "background"]

class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = ["comming_soon", "release_date"]

class QAppNameSerializer(serializers.Serializer):
    name = serializers.CharField()