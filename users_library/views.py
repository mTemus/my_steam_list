from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from games_library.models import AppData
from users_library.models import Collection, UserAppData

from users_library.serializers import UserAppDataCreateSerializer, UserAppDataSerializer
# Create your views here.

class UserAppDataGenericView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserAppDataSerializer

    def get_queryset(self):
        user = self.request.user
        return UserAppData.objects.filter(user=user)

    @action(methods=['post'], detail=False, url_path='app', url_name='add_app')
    def add_app_to_user(self, request):
        query = request.data
        query_serializer = UserAppDataCreateSerializer(data=query)
        
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status.HTTP_400_BAD_REQUEST)

        user_app_data = self._create_user_app_data(query, request.user)
        serializer = UserAppDataSerializer(user_app_data)
        return Response(serializer.data, status.HTTP_200_OK)

    def _create_user_app_data(self, data, user):
        app_data = AppData.objects.get(app_id=data.get("app_data"))
        collections = self._create_collections(data)

        app = UserAppData.objects.create(
            name = f"{user.username} - {app_data.name}",
            status = data.get("status"),
            score = data.get("score"),
            start_date = data.get("start_date"),
            end_date =  data.get("end_date"),
            hours_spent = data.get("hours_spent")
        )
        app.user = user
        app.app_data = app_data
        app.collections.set(collections)
        app.save()
        return app

    def _create_collections(self, data):
        collection_names = data.get("collections")
        collections = [Collection(name=collection) for collection in collection_names]
        Collection.objects.bulk_create(collections)
        return Collection.objects.filter(name__in=collection_names)