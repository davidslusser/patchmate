from django.urls import reverse
from django.db import models as models
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
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

# shared variables
day_choices = (('Sunday','Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
               ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), )
status_choices = (("pending", "pending"), ("cancelled", "cancelled"), ("started", "started"), ("completed", "completed"), )
result_choices = (("unknown", "unknown"), ("cancelled", "cancelled"), ("success", "success"), ("error", "error"), )


class ServiceConfiguration(PatchMateBase):
    """ table to track services """
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    patching_enabled = models.BooleanField(default=False, help_text="enable/disable patching on this service")
    patch_user = models.CharField(max_length=32, default="patch", help_text="name of user used to execute patching scripts")
    script_path = models.CharField(max_length=64, default="/opt/patchmate/service_control_scripts", help_text="location on hosts where service control scripts live")
    patch_frequency = models.IntegerField(default=60, help_text="frequency, in days, of how often patch events should take place")
    min_percent_in_service = models.IntegerField(default=0, help_text="percent of hosts in this service that must remain in service")
    max_percent_out_of_service = models.IntegerField(default=10, help_text="percent of hosts in this service that can be out of service")
    max_percent_daily_patch = models.IntegerField(default=10, help_text="percent of hosts that can be patched in a single day")
    email = models.EmailField(max_length=128, blank=True, null=True, help_text="email address used for alerts and communication")
    im_channel = models.EmailField(max_length=128, blank=True, null=True, help_text="IM channel used for alerts and communication")
    retry_count = models.IntegerField(default=0, help_text="number of retry attempts to make on patch failure")


class ServiceAppControl(PatchMateBase):
    """ table to identify and enable/disable application control scripts """
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    in_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the in_service app control script")
    out_of_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the out_of_service app control script")
    start_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the start_service app control script")
    stop_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the stop_service app control script")
    verify_in_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the verify_in_service app control script")
    verify_out_of_service = models.BooleanField(default=True, blank=True, null=True, help_text="run the verify_out_of_service app control script")
    verify_started = models.BooleanField(default=True, blank=True, null=True, help_text="run the verify_started app control script")
    verify_stopped = models.BooleanField(default=True, blank=True, null=True, help_text="run the verify_stopped app control script")


class ServiceAlert(PatchMateBase):
    """ alerting controls for various events/scenarios"""
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    enable_email_alerts = models.BooleanField(default=False, help_text="enable email alerts")
    enable_im_alerts = models.BooleanField(default=False, help_text="enable IM alerts")
    email_on_patch_success = models.BooleanField(default=False, help_text="send email when patching completes successfully on a host")
    email_on_patch_error = models.BooleanField(default=False, help_text="send email when patching fails on host")
    email_on_step_success = models.BooleanField(default=False, help_text="send email if a any patching step fails")
    im_on_patch_success = models.BooleanField(default=False, help_text="send message when patching completes successfully on a host")
    im_on_patch_error = models.BooleanField(default=False, help_text="send email when patching fails on host")
    im_on_step_error = models.BooleanField(default=False, help_text="send email if a any patching step fails")
    daily_digest = models.BooleanField(default=False, help_text="email a daily digest of patching events that occurred on this service")
    weekly_digest = models.BooleanField(default=False, help_text="email a weekly digest of patching events that occurred on this service")
    weekly_digest_day = models.CharField(max_length=16, choices=day_choices, help_text="day of week to send weekly digest email")


class PatchPool(PatchMateBase):
    """ table to track pools for a Service """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, help_text="name of this pool")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this patching pool")
    hostname_regex = models.CharField(max_length=255, unique=True, help_text="regex pattern for hosts in this pool")
    patching_enabled = models.BooleanField(default=False, help_text="enable patching on this pool")

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
    name = models.CharField(max_length=32, help_text="name of this patching schedule")
    patching_enabled = models.BooleanField(default=False, help_text="enable patching on this pool")
    start_day = models.CharField(max_length=16,
                                 default="Monday",
                                 choices=day_choices,
                                 help_text="day of week this schedule starts")
    start_hour = models.IntegerField(default=8,
                                     validators=[MinValueValidator(0), MaxValueValidator(23)],
                                     help_text="hour of day this schedule starts")
    start_minute = models.IntegerField(default=0,
                                       validators=[MinValueValidator(0), MaxValueValidator(60)],
                                       help_text="minute of hour this schedule starts")
    end_day = models.CharField(max_length=16,
                               default="Monday",
                               choices=day_choices,
                               help_text="day of week this schedule starts")
    end_hour = models.IntegerField(default=5,
                                   validators=[MinValueValidator(0), MaxValueValidator(23)],
                                   help_text="hour of day this schedule starts")
    end_minute = models.IntegerField(default=0,
                                     validators=[MinValueValidator(0), MaxValueValidator(60)],
                                     help_text="minute of hour this schedule starts")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('pool', 'name'), )


class PackageWhitelist(PatchMateBase):
    """ """
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, help_text="name of this service")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this whitelist entry")
    package_regex = models.CharField(max_length=64, blank=True, null=True, help_text="package regex")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('service', 'name'), )


class PatchQueue(PatchMateBase):
    """ table to track patching scheduled patch events """
    host = models.ForeignKey(Host, help_text="host that patching will occur on")
    priority = models.IntegerField(default=9, help_text="priority in the que (0-9, with 0 as the highest priority)")


class PatchEvent(models.Model):
    """ table to track patch events """
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=status_choices)
    completed = models.NullBooleanField(default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="date/time when this event started")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="date/time when this event updated")


class PatchEvenStep(models.Model):
    """ track individual steps of a patching event """
    patch_event = models.ForeignKey(PatchEvent, on_delete=models.CASCADE)
    description = models.CharField(max_length=64, blank=True, null=True, help_text="description of this patch step")
    order = models.IntegerField(blank=True, null=True, help_text="identifies order in the patch process this step takes place")
    status = models.CharField(max_length=16, choices=status_choices, help_text="status of this step")
    result = models.CharField(max_length=16, choices=result_choices, help_text="result of this step")
    completed = models.NullBooleanField(default=None)
    output = models.TextField(blank=True, null=True, help_text="details or output from this step")
    details = models.TextField(blank=True, null=True, help_text="optional details about this patching step")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="date/time when this event started")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="date/time when this event updated")
