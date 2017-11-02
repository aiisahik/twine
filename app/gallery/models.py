from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, HStoreField
from account.models import Profile
from base.models import DateAwareMixin

IMAGE_TYPES = (
    ('png', 'png'),
    ('jpg', 'jpg'),
    ('tiff', 'tiff'),
)

DELETE_REASONS = (
    ('user_remove', 'User Removed'),
    ('offensive', 'Offensive'),
    ('nudity', 'Nudity'),
    ('fake', 'Fake'),
)

class ImageBase(models.Model):
    uploader = models.ForeignKey(Profile, 
        on_delete=models.CASCADE, 
        related_name="uploaded_photos")
    create_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(null=True, blank=True)
    deleter = models.ForeignKey(Profile, 
        on_delete=models.CASCADE, 
        related_name="deleted_photos")
    delete_reason = models.CharField(max_length=20,
        choices=DELETE_REASONS,
        default='user_removed')
    original_filename = models.CharField(max_length=300, null=True, blank=True)
    path = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=10,
        choices=IMAGE_TYPES,
        default='jpg')

    class Meta:
        abstract = True

class Gallery(DateAwareMixin):
    name = models.CharField(max_length=300, null=True, blank=True)
    target = models.ForeignKey(Profile, 
        on_delete=models.CASCADE, 
        related_name="profile_galleries")
    data = HStoreField(null=True, blank=True)
    json_data = JSONField(null=True, blank=True)

class GalleryPhoto(ImageBase):
    order = models.PositiveSmallIntegerField(default=5)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="photos")
    caption = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        ordering = ['order', '-create_date']
