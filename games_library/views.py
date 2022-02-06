from types import NoneType
import requests

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .models import AppEntityData, Category, Entity, Genre, ImageData, Release
from .serializers import AppEnntityDataSerializer, QAppNameSerializer

# Create your views here.

STEAM_ALL_APPS = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
STEAM_APP_DETAILS = 'https://store.steampowered.com/api/appdetails'
STEAM_STORE_APP = 'https://store.steampowered.com/app/'

# update_date = datetime.datetime(0, 0, 0)

all_apps_data = None

class AppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    queryset = AppEntityData.objects.all()
    serializer_class = AppEnntityDataSerializer

    @action(methods=['post'], detail=False, url_path='name', url_name='get_by_name', serializer_class=QAppNameSerializer)
    def get_apps_by_name(self, request):

        # [x] 1. Get apps ids 
        # [x] 2. Try to get apps from db (cached data)
        # [x] 3. Check which ids were querried from db, substract from list
        # [x] 4. Get apps details from steam api
            # [x] 5. Filter unsuccessfull requests
            # [x] 6. Extract usable data
            # [ ] 7. Create models based on data
            # [ ] 7.1 Bulk create models
            # [ ] 7.2 Get created models from db filtered by "app_id__in"
            # [ ] 8. Bound models
            # [ ] 9. Return created models
        # [ ] 10. Add created apps models to models querried from db

        query = request.data
        query_serializer = QAppNameSerializer(data=query)

        if not query_serializer.is_valid() or query.get("name") == NoneType:
            return Response(status.HTTP_400_BAD_REQUEST)

        apps_ids = self._get_apps_ids(query.get("name"))

        querried_apps = AppEntityData.objects.filter(app_id__in=apps_ids)
        apps_ids_from_db = [app_data.app_id for app_data in querried_apps]
        apps_to_querry = apps_ids - apps_ids_from_db

        if len(apps_to_querry) == 0:
            serializer = AppEnntityDataSerializer(data=querried_apps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        apps_from_steam = self._get_apps_from_steam(apps_to_querry)

        


        serializer = AppEnntityDataSerializer(data=querried_apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def _get_apps_ids(self, query_name):
        global all_apps_data

        #TODO: it should be refreshed after 24 hours (?)
        if all_apps_data is None: 
            apps_json = requests.get(STEAM_ALL_APPS).json()
            all_apps_data = apps_json.get("applist").get("apps")
        
        return [data.get("appid") for data in all_apps_data if query_name in data.get("name")]

    def _get_apps_from_steam(self, apps_ids):
        raw_data = [self._get_raw_app_details(app_id) for app_id in apps_ids]
        apps_data = self._extract_apps_data(raw_data)






    def _get_raw_app_details(self, app_id):
        requested_app = requests.get(STEAM_APP_DETAILS, params=app_id).json()
        return self._get_item_from_dict(requested_app)

    def _extract_apps_data(self, apps_data):            
        return [self._extract_app_data(app_data) for app_data in self._filter_success_requests(apps_data)]

    def _filter_success_requests(self, apps_data):
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
            "publishers": app_data.get("publishers", ""),
            "platforms": app_data.get("platforms", ""),
            "release_date": app_data.get("release_date", ""),
            "categories": [self._get_item_from_dict_dict(category, "description") for category in app_data.get("categories", {})],
            "genres": [self._get_item_from_dict_dict(genre, "description") for genre in app_data.get("genres", {})],
            }

    def _get_item_from_dict(self, dict):
        key = next(iter(dict))
        return dict.get(key, {})

    def _get_item_from_dict_dict(self, dict_dict, get_keyword):
        return self._get_item_from_dict(dict_dict).get(get_keyword, "")

    def _create_model_with_ids(self, func, models_data):
        models = [func(model_data) for model_data in models_data]
        ids = [model.app_id for model in models]
        return models, ids

    def _create_model_with_names(self, func, models_data):
        models = [func(model_data) for model_data in models_data]
        names = [model.name for model in models]
        return models, names

    def _create_app_entites(self, apps_data):
        appsEntities, app_ids = self._create_model_with_ids(self._create_app_entity_data, apps_data)
        AppEntityData.objects.bulk_create(appsEntities)
        return AppEntityData.objects.filter(app_id__in = app_ids)

    def _create_app_images(self, apps_data):
        appsImages, app_ids = self._create_model_with_ids(self._create_app_image, apps_data) 
        ImageData.objects.bulk_create(appsImages)
        return ImageData.objects.filter(app_id__in = app_ids)

    def _create_entities(self, apps_data):
        entities, names = self._create_model_with_names(self._create_entity, apps_data) 
        Entity.objects.bulk_create(entities)
        return Entity.objects.filter(name__in = names)

    def _create_app_genres(self, apps_data):
        genres, names = self._create_model_with_names(self._create_app_genre, apps_data) 
        Genre.objects.bulk_create(genres)
        return Genre.objects.filter(name__in = names)

    def _create_app_categories(self, apps_data):
        categories, names = self._create_model_with_names(self._create_app_category, apps_data) 
        Category.objects.bulk_create(categories)
        return Category.objects.filter(name__in = names)

    def _create_app_releases(self, apps_data):
        app_releases, app_ids = self._create_model_with_ids(self._create_app_release, apps_data)
        Release.objects.bulk_create(app_releases)
        return Release.objects.filter(app_id__in = app_ids)

    def _create_app_entity_data(self, app_data):
        return AppEntityData(
            app_id = app_data.get("app_id", 0),
            name = app_data.get("name", ""),
            type = app_data.get("type", ""),
            parent_app = None,
            short_desc = app_data.get("short_desc", ""),
            full_desc = app_data.get("full_desc", ""),
            about = app_data.get("about", ""),
            images = None,
            release = None,
        )

    def _create_app_dlc(self, app_data):
        pass

    def _create_app_image(self, app_data):
        return ImageData(
            app_id = app_data.get("app_id"),
            header = app_data.get("images",{}).get("header",""),
            background = app_data.get("images",{}).get("background",""),
        )

    def _create_entity(self, app_data, entity_category):
        return [Entity(name=entity) for entity in app_data.get(entity_category)]

    def _create_app_genre(self, app_data):
        return [Genre(name=genre) for genre in app_data.get("genres")]

    def _create_app_category(self, app_data):
        return [Category(name=category) for category in app_data.get("categories")]

    def _create_app_release(self, app_data):
        return Release(
            app_id = app_data.get("app_id"),
            comming_soon = app_data.get("release_date", {}).get("coming_soon"),
            release_date = app_data.get("release_date", {}).get("date"),
        )



    

    

    

    
    
    