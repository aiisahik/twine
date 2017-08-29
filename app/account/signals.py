import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from battle.tools import create_battles_for_judge

@receiver(post_save, sender=models.Profile)
def generate_battles_for_new_judge(sender, instance, **kwargs):
    print "received signal for ", instance
    create_battles_for_judge.apply_async(instance, retry=True, retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    })