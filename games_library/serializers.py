from rest_framework import serializers
from games_library.models import AppData, Category, Developer, Genre, ImageData, Publisher, Release

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ["name"]

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = ["header", "background"]

class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = ["comming_soon", "release_date"]

class QAppSerializer(serializers.Serializer):
    q = serializers.CharField()

class AppDataSerializer(serializers.ModelSerializer):
    images = ImageDataSerializer(read_only=True, many=False)
    developers = DeveloperSerializer(read_only=True, many=True)
    publishers = PublisherSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)
    release = ReleaseSerializer(read_only=True, many=False)

    class Meta:
        model = AppData
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