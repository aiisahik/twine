from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PhotoTag(models.Model):
	name = models.CharField(max_length=200)

class ProfilePhoto(models.Model):
	location = models.CharField(max_length=2000)
