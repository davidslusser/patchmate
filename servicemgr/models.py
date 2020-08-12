from django.db import models
from django.contrib.auth.models import Group

from patchmate.models import PatchMateBase


class Owner(PatchMateBase):
    """ owner table """
    name = models.CharField(max_length=32, unique=True, help_text="name of this group")
    group = models.ForeignKey(Group, help_text="group this owner belongs to", on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True, help_text="group email alias for group")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class Service(PatchMateBase):
    """ table to track services """
    name = models.CharField(max_length=255, unique=True, help_text="name of this service")
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this service")

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name
