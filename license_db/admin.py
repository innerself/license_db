from django.contrib import admin

from .models import (
    License, LicenseLocation, LicenseCategory, LicenseType
)


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'modified', 'created')


admin.site.register(License, LicenseAdmin)
admin.site.register(LicenseCategory)
admin.site.register(LicenseLocation)
admin.site.register(LicenseType)
