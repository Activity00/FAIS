from django.contrib import admin

from fa import models


# Register your models here.

class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display=('name',)

class EquipmentPositionAdmin(admin.ModelAdmin):
    list_display=('name',)

admin.site.register(models.EquipmentBasticInfo)
admin.site.register(models.EquipmentType,EquipmentTypeAdmin) 
admin.site.register(models.EquipmentPosition,EquipmentPositionAdmin)

