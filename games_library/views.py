from types import NoneType
import requests

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .models import AppCategory, AppDeveloper, AppDlc, AppData, AppGenre, AppPublisher, Category, Genre, ImageData, Release, Publisher, Developer
from .serializers import AppDataSerializer, QAppNameSerializer

# Create your views here.

STEAM_ALL_APPS = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
STEAM_APP_DETAILS = 'https://store.steampowered.com/api/appdetails'
STEAM_STORE_APP = 'https://store.steampowered.com/app/'

# update_date = datetime.datetime(0, 0, 0)

all_apps_data = None

class AppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    @action(methods=['post'], detail=False, url_path='name', url_name='get_by_name', serializer_class=QAppNameSerializer)
    def querry_apps_by_name(self, request):

        # [x] 1. Get apps ids 
        # [x] 2. Try to get apps from db (cached data)
        # [x] 3. Check which ids were querried from db, substract from list
        # [x] 4. Get apps details from steam api
            # [x] 5. Filter unsuccessfull requests
            # [x] 6. Extract usable data
            # [x] 7. Create models based on data
            # [x] 7.1 Bulk create models
            # [x] 7.2 Get created models from db filtered by "app_id__in"
            # [x] 8. Bound models
            # [x] 9. Return created models
        # [x] 10. Add created apps models to models querried from db

        query = request.data
        query_serializer = QAppNameSerializer(data=query)

        if not query_serializer.is_valid() or query.get("name") == NoneType:
            return Response(status.HTTP_400_BAD_REQUEST)

        apps_ids = self._get_apps_ids(query.get("name"))

        querried_apps = self.get_apps_by_ids(apps_ids)
        serializer = AppDataSerializer(data=querried_apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_apps_by_ids(self, apps_ids):
        apps_from_db = AppData.objects.filter(app_id__in=apps_ids)
        apps_ids_from_db = [app_data.app_id for app_data in apps_from_db]
        apps_to_querry = [id for id in apps_ids if id not in apps_ids_from_db]
        
        if len(apps_to_querry) == 0:
            return apps_from_db

        apps_from_steam = self._get_apps_from_steam(apps_to_querry)
        return apps_from_db | apps_from_steam

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
        return self._create_and_bound_data(apps_data)
        
    def _get_item_from_list_appid(self, id, collection):
        print(id, collection)
        print("================================")

        return next((item for item in collection if item.app_id == id), None)

    def _get_item_from_list_name(self, name, collection):
        return next((item for item in collection if item.name == name), None)

    def _create_and_bound_data(self, apps_data):

        apps = self._create_apps(apps_data)
        dlcs = self._create_dlcs(apps_data)
        images = self._create_app_images(apps_data)
        publishers = self._create_publishers(apps_data)
        developers = self._create_developers(apps_data)
        genres = self._create_genres(apps_data)
        categories = self._create_categories(apps_data)
        releases = self._create_app_releases(apps_data)
        app_dlcs = []
        app_developers = []
        app_publishers = []
        app_genres = []
        app_categories = []

        for app_data in apps_data:
            app = self._get_item_from_list_appid(app_data.get("app_id"), apps)

            app.release = self._get_item_from_list_appid(app.app_id, releases)
            app.images = self._get_item_from_list_appid(app.app_id, images)

            app_dlcs += self._create_app_dlcs(app, app_data, dlcs)
            app_developers += self._create_app_developers(app, app_data, developers)
            app_publishers += self._create_app_publishers(app, app_data, publishers)
            app_genres += self._create_app_genres(app, app_data, genres)
            app_categories += self._create_app_categories(app, app_data, categories)
            
        AppDlc.objects.bulk_create(app_dlcs, ignore_conflicts=True)
        AppDeveloper.objects.bulk_create(app_developers, ignore_conflicts=True)
        AppPublisher.objects.bulk_create(app_publishers, ignore_conflicts=True)
        AppGenre.objects.bulk_create(app_genres, ignore_conflicts=True)
        AppCategory.objects.bulk_create(app_categories, ignore_conflicts=True)

        return apps

    def _get_element(self, name, collection):
        return next((element for element in collection if element.name == name), None)

    def _get_raw_app_details(self, app_id):
        requested_app = requests.get(STEAM_APP_DETAILS, params={"appids":app_id}).json()
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
            "images": {"header": app_data.get("header_image", ""), "background": app_data.get("background", "")},
            "developers": app_data.get("developers", ""),
            "publishers": app_data.get("publishers", "") if app_data.get("publishers", "")[0] != "" else app_data.get("developers", "")[0],
            "platforms": app_data.get("platforms", ""),
            "release_date": app_data.get("release_date", ""),
            "categories": [category.get("description") for category in app_data.get("categories", {})],
            "genres": [genre.get("description") for genre in app_data.get("genres", {})],
            }

    def _get_item_from_dict(self, dict):
        key = next(iter(dict))
        return dict.get(key, {})

    def _get_items_from_list_list(self, list_list):
        return [item for first_list in list_list for item in first_list]

    def _create_model_with_ids(self, func, models_data):
        models = [func(model_data) for model_data in models_data]
        ids = [model.app_id for model in models]
        return models, ids

    def _create_model_with_names(self, func, models_data):
        models = [func(model_data) for model_data in models_data]
        models = self._get_items_from_list_list(models)
        names = [model.name for model in models]
        return models, names

    def _create_apps(self, apps_data):
        appsEntities, app_ids = self._create_model_with_ids(self._create_app_data, apps_data)
        AppData.objects.bulk_create(appsEntities, ignore_conflicts=True)
        return AppData.objects.filter(app_id__in = app_ids)

    def _create_app_images(self, apps_data):
        appsImages, app_ids = self._create_model_with_ids(self._create_app_image, apps_data) 
        ImageData.objects.bulk_create(appsImages, ignore_conflicts=True)
        return ImageData.objects.filter(app_id__in = app_ids)

    def _create_publishers(self, apps_data):
        publishers, names = self._create_model_with_names(self._create_publisher, apps_data)
        Publisher.objects.bulk_create(publishers, ignore_conflicts=True)
        return Publisher.objects.filter(name__in = names)

    def _create_developers(self, apps_data):
        developers, names = self._create_model_with_names(self._create_developer, apps_data)
        Developer.objects.bulk_create(developers, ignore_conflicts=True)
        return Developer.objects.filter(name__in = names)

    def _create_genres(self, apps_data):
        genres, names = self._create_model_with_names(self._create_app_genre, apps_data)
        Genre.objects.bulk_create(genres, ignore_conflicts=True)
        return Genre.objects.filter(name__in = names)

    def _create_categories(self, apps_data):
        categories, names = self._create_model_with_names(self._create_app_category, apps_data)
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        return Category.objects.filter(name__in = names)

    def _create_app_releases(self, apps_data):
        app_releases, app_ids = self._create_model_with_ids(self._create_app_release, apps_data)
        Release.objects.bulk_create(app_releases, ignore_conflicts=True)
        return Release.objects.filter(app_id__in = app_ids)

    def _create_app_data(self, app_data):
        return AppData(
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

    def _create_dlcs(self, apps_data):
        return [self.get_apps_by_ids(app_data.get("dlc")) for app_data in apps_data]

    def _create_app_image(self, app_data):
        return ImageData(
            app_id = app_data.get("app_id"),
            header = app_data.get("images",{}).get("header",""),
            background = app_data.get("images",{}).get("background",""),
        )

    def _create_developer(self, app_data):
        return [Developer(name=developer) for developer in app_data.get("developers")]

    def _create_publisher(self, app_data):
        return [Publisher(name=publisher) for publisher in app_data.get("publishers")]

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

    def _create_app_dlcs(self, app, app_data, dlcs):
        created_dlcs = [AppDlc(
                name = f"{app.name} - dlc_id: {dlc_id}",
                app = app, 
                dlc = self._get_item_from_list_appid(dlc_id, dlcs)
                ) 
                for dlc_id in app_data.get("dlc")]

        for dlc in created_dlcs: dlc.parent_app = app.app_id
        return created_dlcs

    def _create_app_developers(self, app, app_data, developers):
        return [AppDeveloper(
                name = f"{app.name}: {developer}",
                app = app, 
                developer = self._get_item_from_list_name(developer, developers)
                ) 
                for developer in app_data.get("developers")]

    def _create_app_publishers(self, app, app_data, publishers):
       return [AppPublisher(
            name = f"{app.name}: {publisher}",
            app = app, 
            publisher = self._get_item_from_list_name(publisher, publishers)
            ) for publisher in app_data.get("publishers")]

    def _create_app_genres(self, app, app_data, genres):
        return [AppGenre(
            name = f"{app.name}: {genre}",
            app = app,
            genre = self._get_item_from_list_name(genre, genres)
            ) for genre in app_data.get("genres")]

    def _create_app_categories(self, app, app_data, categories):
        return [AppCategory(
            name = f"{app.name}: {category}",
            app = app,
            category = self._get_item_from_list_name(category, categories)
            ) for category in app_data.get("categories")]