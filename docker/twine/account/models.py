from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q



class Profile(models.Model):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

	user = models.OneToOneField(User, primary_key=True)
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
		from twine.rank.models import Player
		Player.objects.update_player_rankings(self)

	def generate_random_match(self):
		from twine.rank.models import Match
		new_match = Match.objects.generate_random_match(judge=self)
		return new_match
	def generate_random_matches(self, num):
		from twine.rank.models import Match
		Match.objects.generate_random_matches(judge=self, num=num)

	def get_matches(self):
		import datetime
		from twine.rank.models import Match
		date_now = datetime.datetime.now()
		profile_matches = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('create_date').all()
		return profile_matches

	def get_latest_match(self):
		import datetime
		from twine.rank.models import Match
		date_now = datetime.datetime.now()
		latest_profile_match = Match.objects.filter(
			Q(expire_date=None) | Q(expire_date__gt=date_now),
			Q(winner=self) | Q(loser=self)).order_by('-create_date')[:1].first()
		return latest_profile_match


# Create your models here.
