from django.http import HttpResponse
import requests

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .models import AppData
from .serializers import AppDataSerializer, QAppNameSerializer

# Create your views here.

STEAM_ALL_APPS = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
STEAM_APP_DETAILS = 'https://store.steampowered.com/api/appdetails?appids='

# update_date = datetime.datetime(0, 0, 0)

all_apps_data = None

class AppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    @action(methods=['post'], detail=False, url_path='all', url_name='allapps', serializer_class=QAppNameSerializer)
    def get_apps(self, request):
        global all_apps_data

        if all_apps_data is None:
            apps_json = requests.get(STEAM_ALL_APPS).json()
            all_apps_data = apps_json.get("applist").get("apps")
        
        query = request.data
        query_serializer = QAppNameSerializer(data=query)

        if not query_serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        query_name = query.get("name")
        query_apps = [self._create_app_data(data) for data in all_apps_data if query_name in data.get("name")]
        print(type[query_apps[0]])
        
        serializer = AppDataSerializer(query_apps, many=True)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def _create_app_data(self, app_data):
        return AppData(
            app_id = app_data.get("appid"), 
            name = app_data.get("name")
            )