from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import DateAwareMixin

class ProfileManager(models.Manager):
	def get_matches(self, judge): 
		date_now = timezone.now() 
		min_age_date = date_now - timedelta(days=judge.min_age_preference*365) 
		max_age_date = date_now - timedelta(days=judge.max_age_preference*365) 
		age_filter = Q(dob__gte=max_age_date, dob__lte=min_age_date)
		preferred_traits = [preference.trait_id for preference in TraitPreference.active.filter(profile=judge)]
		if len(preferred_traits) > 0:
			trait_preference_filter = Q(trait_identities__trait_id__in=preferred_traits)
		else: 
			trait_preference_filter = Q()
		if judge.gender_preference == "BI":
			gender_filter = (Q(gender=judge.gender) & Q(gender_preference=judge.gender)) | Q(gender_preference="BI")
		else:
			gender_filter = Q(gender=judge.gender_preference, gender_preference=judge.gender)
		matches = self.filter(
			age_filter,
			gender_filter,
			trait_preference_filter,
		).exclude(user_id=judge.user_id)
		return matches

class Profile(models.Model):
	GENDER_CHOICES = (
	    ('M', 'Male'),
        ('F', 'Female')
    )
	GENDER_PREFERENCE_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
		('BI', 'Bisexual'),
    )

	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)

	dob = models.DateTimeField(null=True, blank=True)
	min_age_preference = models.PositiveSmallIntegerField(null=False, default=18, blank=False)
	max_age_preference = models.PositiveSmallIntegerField(null=False, default=99, blank=False)

	gender = models.CharField(max_length=10,
									choices=GENDER_CHOICES,
									default='F')
	gender_preference = models.CharField(max_length=10,
									choices=GENDER_PREFERENCE_CHOICES,
									default='M')
	height = models.PositiveSmallIntegerField(null=True, blank=True) # height in cm
	min_height_preference = models.PositiveSmallIntegerField(null=True, blank=True)
	max_height_preference = models.PositiveSmallIntegerField(null=True, blank=True)

	objects = ProfileManager()

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

class TraitType(models.Model):
	name = models.CharField(max_length=200, null=False, blank=False)
	label = models.CharField(max_length=200, null=True, blank=True)

class Trait(models.Model):
	name = models.CharField(max_length=200, null=False, blank=False)
	label = models.CharField(max_length=200, null=True, blank=True)
	type = models.ForeignKey(TraitType, related_name="trait_type")
	parent_type = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

class TraitPreference(DateAwareMixin):
	profile = models.ForeignKey(Profile)
	strength = models.PositiveSmallIntegerField(null=False, default=5, blank=False)
	trait = models.ForeignKey(Trait, related_name="preference_traits")

class TraitIdentity(DateAwareMixin):
	profile = models.ForeignKey(Profile, related_name="trait_identities")
	strength = models.PositiveSmallIntegerField(null=False, default=5, blank=False)
	trait = models.ForeignKey(Trait, related_name="identity_traits")

class PreferenceMatch(DateAwareMixin):
	profile = models.ForeignKey(Profile, related_name="matches")
	target = models.ForeignKey(Profile, related_name="target_matches")
	mutual = models.BooleanField(default=False)

class Group(DateAwareMixin):
	name = models.CharField(max_length=256)
	members = models.ManyToManyField(
		Profile,
		related_name="groups",
		through='GroupMembership',
		through_fields=('group', 'member'),
	)

	def get_admins(self):
		memberships = GroupMembership.active.filter(group=self, membership_type='admin')
		return Profile.objects.filter(user_id__in=[member.user_id for member in memberships])
	
	def get_founder(self):
		founder_membership = GroupMembership.active.filter(group=self, membership_type='founder').select_related('member').first()
		if founder_membership: 
			return founder_membership.member
		else: 
			return None

	def add_members(self, new_members, membership_type="member", inviter=None):
		GroupMembership.objects.filter(member__in=new_members)
		new_memberships = []
		for member in new_members:
			new_memberships.append(GroupMembership(
				member=member, 
				group=self, 
				inviter=inviter,
				membership_type=membership_type,
				start_date=timezone.now()
			))
		new_memberships = GroupMembership.objects.bulk_create(new_memberships)
		return new_memberships
	
	def remove_members(self, removed_members, remover):
		remover_membership = GroupMembership.active.filter(
			member=remover, 
			group=self, 
			membership_type__in=['admin', 'founder'])
		if remover_membership.count() > 0:
			memberships = GroupMembership.active.filter(member__in=removed_members, group=self)
			for membership in memberships:
				membership.end(commit=True)
		else: 
			raise Exception("Not authorized to remove members")

MEMBERSHIP_TYPE_CHOICES = (
	('admin', 'Administrator'),
	('founder', 'Founder'),
	('member', 'Member'),
)

class GroupMembership(DateAwareMixin):
	group = models.ForeignKey(
		Group, 
		on_delete=models.CASCADE, 
		related_name="group_memberships"
	)
	member = models.ForeignKey(
		Profile, 
		on_delete=models.CASCADE, 
		related_name="memberships"
	)
	inviter = models.ForeignKey(
		Profile,
		null=True, 
		blank=True,
		related_name="inviter_memberships",
	)
	membership_type = models.CharField(
		max_length=10,
		choices=MEMBERSHIP_TYPE_CHOICES,
		default='member'
	)

@receiver(post_save, sender=Profile)
def generate_battles_for_new_judge(sender, instance, **kwargs):
	print "received signal for ", instance
	from battle.tools import create_battles_for_judge
	create_battles_for_judge.apply_async(instance, retry=True, retry_policy={
		'max_retries': 3,
		'interval_start': 0,
		'interval_step': 0.2,
		'interval_max': 0.2,
	})
