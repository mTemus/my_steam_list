from rest_framework.routers import DefaultRouter

from users_library.views import UserAppDataGenericView


router = DefaultRouter()
router.register(r'add', UserAppDataGenericView, basename='addapp')

urlpatterns = router.urls