from django.contrib import admin

# import models
from patchmgr.models import (ServiceControl,
                             PatchPool,
                             PatchPoolRule,
                             PatchSchedule,
                             PackageWhitelist,
                             PatchQueue,
                             PatchEvent
                             )


class ServiceControlAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'alerts_email', 'alerts_slack', 'patching_enabled', 'script_path', 'patch_frequency', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    search_fields = ['service', 'script_path', 'patch_frequency', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    list_filter = ['active', 'alerts_email', 'alerts_slack', 'patching_enabled']


class PatchPoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'name', 'description', 'hostname_regex', 'enabled']
    search_fields = ['name', 'description', 'hostname_regex']
    list_filter = ['active', 'service', 'enabled']


class PatchPoolRuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'pool', 'name', 'patching_enabled', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    search_fields = ['name', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    list_filter = ['active', 'pool', 'patching_enabled']


class PatchScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'pool', 'name', 'start_datetime', 'end_datetime', 'enabled']
    search_fields = ['name']
    list_filter = ['active', 'pool', 'enabled']


class PackageWhitelistAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'name', 'description', 'package_regex', 'enabled']
    search_fields = ['name', 'description', 'package_regex']
    list_filter = ['active', 'service', 'enabled']


class PatchQueueAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active']
    search_fields = []
    list_filter = ['active']


class PatchEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active']
    search_fields = []
    list_filter = ['active']


# register models
admin.site.register(ServiceControl, ServiceControlAdmin)
admin.site.register(PatchPool, PatchPoolAdmin)
admin.site.register(PatchPoolRule, PatchPoolRuleAdmin)
admin.site.register(PatchSchedule, PatchScheduleAdmin)
admin.site.register(PackageWhitelist, PackageWhitelistAdmin)
admin.site.register(PatchQueue, PatchQueueAdmin)
admin.site.register(PatchEvent, PatchEventAdmin)
