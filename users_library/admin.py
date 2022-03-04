from django.contrib.auth.models import Group
from django.contrib import admin

from users_library.models import UserAccount, UserAppData

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserAppData)
