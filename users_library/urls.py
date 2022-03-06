from rest_framework.routers import DefaultRouter

from users_library.views import AddAppDataToUser, DeleteAppDataOfCurrUser, ListAppDataOfCurrUser, UpdateAppDataOfCurrUser


router = DefaultRouter()
router.register(r'', AddAppDataToUser, basename='addapp')
router.register(r'list', ListAppDataOfCurrUser, basename='listapps')
router.register(r'update', UpdateAppDataOfCurrUser, basename='updateapp')
router.register(r'delete', DeleteAppDataOfCurrUser, basename='deleteapp')

urlpatterns = router.urls