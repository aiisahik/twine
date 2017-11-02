import models
import names
from django.contrib.auth.models import User
from battle.models import Battle, Player
from account.models import Profile, PreferenceMatch
import random
import hashlib
from datetime import datetime

def generate_battles_for_all(num=100):
    profiles = Profile.objects.all()
    for profile in profiles:
        battles = create_battles_for_judge(profile, num=num)
        print "%d battles for: %s %s" % (len(battles), profile.first_name, profile.last_name)
    print "==== done ===" 

def create_battles_for_judge(judge):
    from itertools import combinations
    existing_battles_matrix = {}
    existing_battles = Battle.objects.filter(judge=judge, pick_date__isnull=True)

    for battle in existing_battles: 
        if battle.left.user_id > battle.right.user_id:   
            existing_battles_matrix[battle.right.user_id] = battle.left.user_id
        else:
            existing_battles_matrix[battle.left.user_id] = battle.right.user_id
    
    preference_matches = PreferenceMatch.active.filter(profile=judge)
    target_profiles = [match.target for match in preference_matches]
    possible_battle_pairs = combinations(target_profiles, 2)

    new_battles = []
    for pair in possible_battle_pairs:
        if pair[0].user_id > pair[1].user_id:
            has_existing_battle = existing_battles_matrix.get(pair[1].user_id, None)
        else: 
            has_existing_battle = existing_battles_matrix.get(pair[0].user_id, None)
        if not has_existing_battle: 
            new_battles.append(Battle(
                judge=judge,
                left=pair[1],
                right=pair[0]
            ))
    created_battles = Battle.objects.bulk_create(new_battles)
    print "created %d battles" % len(created_battles)
    return created_battles