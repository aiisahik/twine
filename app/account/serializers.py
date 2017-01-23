from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime
from . import models

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Profile.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('user','first_name', 'last_name', 'dob', 'gender', 'gender_preference')
        read_only_fields = ('user',)
