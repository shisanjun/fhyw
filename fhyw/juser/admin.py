from django.contrib import admin
from juser import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)
admin.site.register(models.Menu)
admin.site.register(models.Menu2)
admin.site.register(models.Role)
