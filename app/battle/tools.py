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
    target_profiles = Profile.objects.get_matches(judge)
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

def generate_random_battle(judge):
    profile_count = Profile.objects.filter(gender=judge.gender_preference).count()
    random_index_1 = randint(0, profile_count - 1)
    random_index_2 = randint(0, profile_count - 2)
    leftProfile = Profile.objects.filter(gender=judge.gender_preference)[random_index_1]
    rightProfile = Profile.objects.filter(gender=judge.gender_preference).exclude(user__id=leftProfile.user_id)[random_index_2]
    new_battle = Battle(left=leftProfile, right=rightProfile, judge=judge)
    return new_battle

def generate_random_battles(judge, num):
    new_battles = []
    for i in [0] * num:
        new_battle = generate_random_battle(judge=judge)
        new_battles.append(new_battle)
    created_battles = Battle.objects.bulk_create(new_battles)