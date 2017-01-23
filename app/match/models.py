from django.db import models
from account.models import Profile

class Match(models.Model):
    a = models.ForeignKey(Profile, related_name="target_a", related_query_name="player_a")
    b = models.ForeignKey(Profile, related_name="target_b", related_query_name="target_b")
    combined_mu = models.FloatField(null=True, blank=True)
    combined_elo = models.FloatField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    def __unicode__(self):
        return "Match: {0} {1} and {2}{3}".format(self.a.first_name, self.a.last_name, self.b.first_name, self.b.last_name)
