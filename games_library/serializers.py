from rest_framework import serializers
from games_library.models import AppData

class AppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppData
        fields = ["app_id", "name"]

class QAppNameSerializer(serializers.Serializer):
    name = serializers.CharField()