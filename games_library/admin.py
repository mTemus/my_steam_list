
from django.contrib import admin
from .models import AppCategory, AppDeveloper, AppDlc, AppData, AppGenre, AppPublisher, Category, Genre, ImageData, Release, Publisher, Developer

# Register your models here.

admin.site.register(AppData)
admin.site.register(AppCategory)
admin.site.register(AppDeveloper)
admin.site.register(AppDlc)
admin.site.register(AppGenre)
admin.site.register(AppPublisher)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(ImageData)
admin.site.register(Release)
admin.site.register(Publisher)
admin.site.register(Developer)