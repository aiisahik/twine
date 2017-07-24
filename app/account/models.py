from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone


class Profile(models.Model):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)

	dob = models.DateTimeField(null=True, blank=True)
	gender = models.CharField(max_length=10,
									choices=GENDER_CHOICES,
									default='F')
	gender_preference = models.CharField(max_length=10,
									choices=GENDER_CHOICES,
									default='M')

	def __unicode__(self):
		return "{0} - {1}".format(self.user.username, self.last_name)

	def update_player_rankings(self):
		from rank.models import Player
		Player.objects.update_player_rankings(self)

	def generate_random_battle(self):
		from rank.models import Battle
		return Battle.objects.generate_random_battle(judge=self)
	def generate_random_battles(self, num):
		from rank.models import Battle
		return Battle.objects.generate_random_battles(judge=self, num=num)

	def get_battles(self):
		from rank.models import Battle
		date_now = timezone.now()
		profile_battles = Battle.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('create_date').all()
		return profile_battles

	def get_latest_battle(self):
		from rank.models import Battle
		date_now = timezone.now()
		latest_profile_battle = Battle.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('-create_date')[:1].first()
		return latest_profile_battle


# Create your models here.
