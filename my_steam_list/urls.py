"""
my_steam_list URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/db/', include('games_library.urls')),
    path('api/user/', include('users_library.urls')),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
]
