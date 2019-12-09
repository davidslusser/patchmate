from django.urls import reverse
from django.db import models as models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils import timezone

from itertools import groupby
from operator import itemgetter

# import third party modules
from auditlog.registry import auditlog

# import patchmate module
from patchmate.models import PatchMateBase
from servicemgr.models import Service
from hostmgr.models import Host


class ServiceControl(PatchMateBase):
    """ table to track services """
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    alerts_email = models.BooleanField(default=False, help_text="enable email alerts")
    alerts_slack = models.BooleanField(default=False, help_text="enable slack alerts")
    patching_enabled = models.BooleanField(default=False, help_text="enable/disable patching on this service")
    script_path = models.CharField(max_length=64, default="/opt/patchmate/service_control_scripts", help_text="location on hosts where service control scripts live")
    patch_frequency = models.IntegerField(default=60, help_text="frequency, in days, of how often patch events should take place")
    min_percent_in_service = models.FloatField(default=0, help_text="percent of hosts in this service that must remain in service")
    max_percent_out_of_service = models.FloatField(default=10, help_text="percent of hosts in this service that can be out of service")
    max_percent_daily_patch = models.FloatField(default=10, help_text="percent of hosts that can be patched in a single day")

    def __unicode__(self):
        return u'%s' % self.service.name

    def __str__(self):
        return self.service.name


class PatchPool(PatchMateBase):
    """ table to track pools for a Service """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, help_text="name of this pool")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this patching pool")
    hostname_regex = models.CharField(max_length=255, unique=True, help_text="regex pattern for hosts in this pool")
    enabled = models.BooleanField(default=False, help_text="enable patching on this pool")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class PatchPoolRule(PatchMateBase):
    """ rules for host selection in a pool """
    pool = models.ForeignKey(PatchPool, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, help_text="name of this patching schedule")
    patching_enabled = models.BooleanField(default=False, help_text="enable patching on this pool")
    min_percent_in_service = models.FloatField(default=0, help_text="percent of hosts in this pool that must remain in service")
    max_percent_out_of_service = models.FloatField(default=10, help_text="percent of hosts in this pool that can be out of service")
    max_percent_daily_patch = models.FloatField(default=10, help_text="percent of hosts in this pool that can be patched in a single day")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class PatchSchedule(PatchMateBase):
    """ table to track schedules for a ServicePool """
    pool = models.ForeignKey(PatchPool, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, help_text="name of this patching schedule")
    start_datetime = models.DateTimeField(help_text="start date and time for this patch schedule")
    end_datetime = models.DateTimeField(help_text="start date and time for this patch schedule")
    enabled = models.BooleanField(default=False, help_text="enable patching on this pool")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class PackageWhitelist(PatchMateBase):
    """ """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, help_text="name of this service")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this whitelist entry")
    package_regex = models.CharField(max_length=64, blank=True, null=True, help_text="package regex")
    enabled = models.BooleanField(default=False, help_text="enable patching on this pool")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

# class HostWhitelist(PatchMateBase):
#     """ """
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     name = models.CharField(max_length=32, unique=True, help_text="name of this service")
#     description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this whitelist entry")
#     hostname_regex = models.CharField(max_length=64, blank=True, null=True, help_text="package regex")
#     enabled = models.BooleanField(default=False, help_text="enable patching on this pool")


class PatchQueue(PatchMateBase):
    """ table to track patching scheduled patch events """
    pass


class PatchEvent(PatchMateBase):
    """ table to track patch events """
    pass
