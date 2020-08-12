from django.contrib import admin

# import models
from servicemgr.models import (Owner,
                               Service
                               )


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'group', 'email']
    search_fields = ['name', 'email']
    list_filter = ['active', 'group']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'owner', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active', 'owner']


# register models
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Service, ServiceAdmin)
