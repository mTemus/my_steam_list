from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin

from users_library.models import UserAccount, UserAppData, UserApps

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserAppData)
admin.site.register(UserApps)

admin.site.unregister(Group)
