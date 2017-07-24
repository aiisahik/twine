from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime
from . import models
from account.serializers import ProfileSerializer

class BattleSerializer(serializers.ModelSerializer):
    left = ProfileSerializer()
    right = ProfileSerializer()
    winner = serializers.PrimaryKeyRelatedField(queryset=models.Player.objects)
    loser = serializers.PrimaryKeyRelatedField(queryset=models.Player.objects)

    class Meta:
        model = models.Battle
        fields = ('id', 'left','right', 'winner', 'loser', 'create_date', 'pick_date')
        read_only_fields = ('left','right', 'create_date', )

class PlayerSerializer(serializers.ModelSerializer):
    judge = ProfileSerializer()
    target = ProfileSerializer()
    class Meta:
        model = models.Battle
        # fields = ('id', 'left','right', 'winner', 'loser', 'create_date', 'pick_date')
        read_only_fields = ('judge','target', )
