from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime
import pytz

DATEAWARE_START_DATE = datetime(1900, 1, 1, 0,0,0,0, pytz.UTC)
DATEAWARE_END_DATE = datetime(3000, 1, 1, 0,0,0,0, pytz.UTC)

class DateAwareManager(models.Manager):

    def active(self, now=None):
        return DateAwareMixin.active_only(self, now=now, try_queryset=True)

class DateAwareActiveManager(models.Manager):

    def get_queryset(self):
        return DateAwareMixin.active_only(
            super(DateAwareActiveManager, self).get_queryset())

class DateAwareMixin(models.Model):
    start_date = models.DateTimeField(default=DATEAWARE_START_DATE, db_index=True)
    end_date = models.DateTimeField(default=DATEAWARE_END_DATE, db_index=True)

    objects = DateAwareManager()
    active = DateAwareActiveManager()

    class Meta:
        abstract = True
        index_together = [
            ['start_date', 'end_date'],
        ]
    
    def is_active(self, now=None):
        if not now:
            now = timezone.now()
        return self.start_date <= now and self.end_date > now
    is_active.boolean = True

    @classmethod
    def active_only(cls, instances, now=None):
        if not now:
            now = timezone.now()
        return instances.filter(start_date__lte=now, end_date__gt=now)
