from django.db import models
from django.contrib.auth.models import Group

from patchmate.models import PatchMateBase
from servicemgr.models import Service


class Host(PatchMateBase):
    """ table to track hosts """
    name = models.CharField(max_length=255, unique=True, help_text="name of this host")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    patching_enabled = models.BooleanField(default=False, help_text="enable/disable patching on this host")
    last_patched_at = models.DateTimeField(blank=True, null=True, help_text="date/time when this host was last patched")
    in_service = models.BooleanField(default=False, help_text="flag to determine if this host is in service")

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name
