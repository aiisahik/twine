import models
import names
from django.contrib.auth.models import User
from battle.models import Battle, Player
from account.models import Profile
import random
import hashlib
from datetime import datetime


def generate_picks_for_judge(judge, num=100):
    battles = Battle.objects.get_battles(judge, num=num)
    for battle in battles:
        left_hash_input = battle.left.user.email + judge.user.email
        right_hash_input = battle.right.user.email + judge.user.email
        left_strength = int(hashlib.sha1(left_hash_input).hexdigest(), 16) % (10 ** 8)
        right_strength = int(hashlib.sha1(right_hash_input).hexdigest(), 16) % (10 ** 8)
        if left_strength > right_strength:
            battle.pick('left')
        else:
            battle.pick('right')

def generate_battles_for_all(num=100):
    profiles = Profile.objects.all()
    for profile in profiles:
        battles = Battle.objects.get_battles(profile, num=num)
        print "%d battles for: %s %s" % (len(battles), profile.first_name, profile.last_name)
    print "==== done ===" 