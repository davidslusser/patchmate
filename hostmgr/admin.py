from django.contrib import admin

# import models
from hostmgr.models import (Host
                            )


class HostAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'service', 'patching_enabled', 'last_patched_at', 'in_service']
    search_fields = ['name']
    list_filter = ['active', 'service', 'patching_enabled', 'in_service']


# register models
admin.site.register(Host, HostAdmin)
