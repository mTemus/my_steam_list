from types import NoneType
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
STEAM_APP_DETAILS = 'https://store.steampowered.com/api/appdetails'
STEAM_STORE_APP = 'https://store.steampowered.com/app/'

# update_date = datetime.datetime(0, 0, 0)

all_apps_data = None
querried_apps = None

class AppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    @action(methods=['post'], detail=False, url_path='all', url_name='allapps', serializer_class=QAppNameSerializer)
    def get_apps_data(self, request):
        global querried_apps

        query = request.data
        query_serializer = QAppNameSerializer(data=query)

        if not query_serializer.is_valid():
            return Response(status.HTTP_400_BAD_REQUEST)

        apps_ids = self._get_app_ids(query.get("name"))
        querried_apps = [self._get_app_details(app_id) for app_id in apps_ids]
        extracted_apps = self._extract_apps_data(querried_apps)
        return Response(extracted_apps, status=status.HTTP_200_OK)
    
    def _get_app_details(self, app_id):
        requested_app = requests.get(STEAM_APP_DETAILS, params=app_id).json()
        app_key = next(iter(requested_app))
        return requested_app.get(app_key)

    def _get_app_ids(self, query_name):
        global all_apps_data

        if all_apps_data is None:
            apps_json = requests.get(STEAM_ALL_APPS).json()
            all_apps_data = apps_json.get("applist").get("apps")
        
        return [{"appids": data.get("appid")} for data in all_apps_data if query_name in data.get("name")]

    def _extract_apps_data(self, apps_data):            
        return [self._extract_app_data(app_data) for app_data in self._filter_apps_data(apps_data)]

    def _filter_apps_data(self, apps_data):
        success_apps = [app_data.get("data") for app_data in apps_data if app_data.get("success")]
        return [app_data for app_data in success_apps if app_data.get("type") != "movie"]

    def _extract_app_data(self, app_data):
        return {
            "app_id": app_data.get("steam_appid", ""),
            "name": app_data.get("name", ""),
            "type": app_data.get("type", ""),
            "parent_app": app_data.get("fullgame", {}).get("appid", 0),
            "dlc": app_data.get("dlc", []),
            "short_desc": app_data.get("short_description", ""),
            "full_desc": app_data.get("detailed_description", ""),
            "about": app_data.get("about_the_game"),
            "images": [{"header": app_data.get("header_image", ""), "background": app_data.get("background", "")}],
            "developers": app_data.get("developers", ""),
            "publisher": app_data.get("publishers", ""),
            "platforms": app_data.get("platforms", ""),
            "release_date": app_data.get("release_date", "")
            }
    
    