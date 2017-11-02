import models
import names
from django.contrib.auth.models import User
from battle.models import Battle, Player
from account.models import Profile, PreferenceMatch
import random
import hashlib
from datetime import datetime

def randomly_pick_winners_for_judge(judge):
    battles = Battle.objects.filter(judge=judge, pick_date__isnull=True)
    for battle in battles:
        left_hash_input = battle.left.user.email + judge.user.email
        right_hash_input = battle.right.user.email + judge.user.email
        left_strength = int(hashlib.sha1(left_hash_input).hexdigest(), 16) % (10 ** 8)
        right_strength = int(hashlib.sha1(right_hash_input).hexdigest(), 16) % (10 ** 8)
        if left_strength > right_strength:
            battle.pick('left')
        else:
            battle.pick('right')
    players = Player.objects.filter(judge=judge).order_by('-mu')
    for rank_index, player in enumerate(players): 
        player.trueskill_rank = rank_index + 1
        player.save()
        # print "player:", player.trueskill_rank, player.mu, player.target. player.target.first_name, player.target.last_name
        print "player:", player.trueskill_rank, player
    return players

    