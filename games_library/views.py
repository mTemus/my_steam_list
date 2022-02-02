from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .models import AppData
from .serializers import AppDataSerializer

# Create your views here.

class AppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    