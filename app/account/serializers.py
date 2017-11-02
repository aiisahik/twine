from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime
from . import models

from django.contrib.auth.models import User

class TraitSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.Trait
        fields = ('name', 'type', )

class TraitIdentitySerializer(serializers.ModelSerializer):
    # queryset = models.TraitIdentity.active.all(),
    trait = TraitSerializer(read_only=True)

    class Meta:
        model = models.TraitIdentity
        fields = ('strength', 'trait', )

class TraitPreferenceSerializer(serializers.ModelSerializer):
    # queryset = models.TraitIdentity.active.all(),
    trait = TraitSerializer(read_only=True)

    class Meta:
        model = models.TraitPreference
        fields = ('strength', 'trait', )


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

class PreferenceMatchSerializer(serializers.ModelSerializer):
    target = ProfileSerializer()
    class Meta:
        model = models.PreferenceMatch
        fields = ('mutual', 'target', )

class FullProfileSerializer(serializers.ModelSerializer):
    trait_identities = serializers.SerializerMethodField()
    trait_preferences = serializers.SerializerMethodField()
    matches = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ('user','first_name', 'last_name', 'dob', 'gender', 'gender_preference', 'trait_identities', 'trait_preferences', 'matches')
        read_only_fields = ('user', 'trait_identities', 'trait_preferences', 'matches')

    def get_trait_identities(self, obj): 
        trait_identities = models.TraitIdentity.active.filter(profile=obj)
        return TraitIdentitySerializer(instance=trait_identities, many=True).data
    
    def get_trait_preferences(self, obj): 
        trait_preferences = models.TraitPreference.active.filter(profile=obj)
        return TraitPreferenceSerializer(instance=trait_preferences, many=True).data

    def get_matches(self,obj):
        matches = models.PreferenceMatch.active.filter(profile=obj).select_related('target')
        return PreferenceMatchSerializer(instance=matches, many=True).data

