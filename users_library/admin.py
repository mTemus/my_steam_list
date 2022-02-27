from django.contrib import admin

from users_library.models import UserAccount, UserAppData, UserApps

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserAppData)
admin.site.register(UserApps)