from django.contrib import admin

# import models
from patchmgr.models import (ServiceControl,
                             PatchPool,
                             PatchPoolRule,
                             PatchSchedule,
                             PackageWhitelist,
                             PatchQueue,
                             PatchEvent,
                             PatchEvenStep
                             )


class ServiceControlAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'alerts_email', 'alerts_slack', 'patching_enabled', 'script_path', 'patch_frequency', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    search_fields = ['service', 'script_path', 'patch_frequency', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    list_filter = ['active', 'alerts_email', 'alerts_slack', 'patching_enabled']


class PatchPoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'name', 'description', 'hostname_regex', 'patching_enabled']
    search_fields = ['name', 'description', 'hostname_regex']
    list_filter = ['active', 'service', 'patching_enabled']


class PatchPoolRuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'pool', 'name', 'patching_enabled', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    search_fields = ['name', 'min_percent_in_service', 'max_percent_out_of_service', 'max_percent_daily_patch']
    list_filter = ['active', 'pool', 'patching_enabled']


class PatchScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'pool', 'name', 'patching_enabled', 'start_day', 'start_hour', 'start_minute', 'end_day', 'end_hour', 'end_minute']
    search_fields = ['name', 'start_day', 'start_hour', 'start_minute', 'end_day', 'end_hour', 'end_minute']
    list_filter = ['active', 'pool', 'patching_enabled', 'start_day', 'end_day']


class PackageWhitelistAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'service', 'name', 'description', 'package_regex']
    search_fields = ['name', 'description', 'package_regex']
    list_filter = ['active', 'service']


class PatchQueueAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active']
    search_fields = []
    list_filter = ['active']


class PatchEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'active', 'host', 'status', 'completed', 'created_at', 'updated_at']
    search_fields = ['status', 'completed']
    list_filter = ['active', 'host', 'status']


class PatchEvenStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'patch_event', 'status', 'result', 'completed', 'output', 'created_at', 'updated_at']
    search_fields = ['status', 'result', 'completed', 'output']
    list_filter = ['patch_event', 'status', 'result']


# register models
admin.site.register(ServiceControl, ServiceControlAdmin)
admin.site.register(PatchPool, PatchPoolAdmin)
admin.site.register(PatchPoolRule, PatchPoolRuleAdmin)
admin.site.register(PatchSchedule, PatchScheduleAdmin)
admin.site.register(PackageWhitelist, PackageWhitelistAdmin)
admin.site.register(PatchQueue, PatchQueueAdmin)
admin.site.register(PatchEvent, PatchEventAdmin)
admin.site.register(PatchEvenStep, PatchEvenStepAdmin)
