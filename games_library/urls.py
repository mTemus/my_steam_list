from django.urls import path, include
from rest_framework.routers import DefaultRouter

from games_library.views import AppDataGenericView

router = DefaultRouter()
router.register(r'apps', AppDataGenericView, basename='apps')

urlpatterns = router.urls