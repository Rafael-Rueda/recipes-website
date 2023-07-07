from django.contrib import admin

from apps.authors import models


class UserLogConfig(admin.ModelAdmin):
    ...

admin.site.register(models.UserLog, UserLogConfig)