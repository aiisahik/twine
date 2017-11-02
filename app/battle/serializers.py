from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime
from . import models
from account.serializers import ProfileSerializer

class PlayerSerializer(serializers.ModelSerializer):
    judge = serializers.PrimaryKeyRelatedField(read_only=True)
    target = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Player
        fields = ('id', "judge", "target", "mu", "sigma", "elo", "trueskill_rank", "elo_rank", )
        read_only_fields = ('judge','target', )

class BattleSerializer(serializers.ModelSerializer):
    left = ProfileSerializer()
    right = ProfileSerializer()
    winner = PlayerSerializer()
    loser = PlayerSerializer()

    class Meta:
        model = models.Battle
        fields = ('id', 'left','right', 'winner', 'loser', 'create_date', 'pick_date')
        read_only_fields = ('left','right', 'create_date', )

