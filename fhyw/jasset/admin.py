from django.contrib import admin
from jasset import models
# Register your models here.


class AssetRecordAdmin(admin.ModelAdmin):
    list_display = ("asset","content","create_time")

admin.site.register(models.IDC)
admin.site.register(models.DeviceType)
admin.site.register(models.Asset)
admin.site.register(models.Host)
admin.site.register(models.HostBasic)
admin.site.register(models.HostCPU)
admin.site.register(models.HostMemory)
admin.site.register(models.HostBoard)
admin.site.register(models.HostGroup)
admin.site.register(models.HostDisk)
admin.site.register(models.HostNIC)
admin.site.register(models.AssetRecord,AssetRecordAdmin)
admin.site.register(models.ErrorLog)

