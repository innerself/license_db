from django.contrib import admin

from .models import License, LicenseType, LicenseSubtype

# admin.site.register(License)


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'modified', 'created')


admin.site.register(License, LicenseAdmin)
admin.site.register(LicenseType)
admin.site.register(LicenseSubtype)
