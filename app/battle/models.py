from django.db import models
from django.contrib.postgres.fields import JSONField, HStoreField
from django.db.models.aggregates import Count
from random import randint
from collections import defaultdict, OrderedDict
from account.models import Profile
from gallery.models import Gallery

from trueskill import Rating, quality_1vs1, rate_1vs1
import elo
import datetime
from django.utils import timezone


class PlayerManager(models.Manager):
    def get_ranked_players(self, judge):
        ranked_players = self.filter(judge=judge).order_by('-mu')
        print ">>>>>> players for ", judge.first_name, judge.last_name, "<<<<<<<"
        for player in ranked_players:
            won_battles = Battle.objects.filter(judge=judge, winner=player)
            print player.mu, player.target.first_name, player.target.last_name
            for won_battle in won_battles:
                print " ======== won against", won_battle.loser.target.first_name, won_battle.loser.target.last_name
        return ranked_players

    def generate_pairings(self):
        from munkres import Munkres
        ## create a matrix of mu values
        matrix = defaultdict(OrderedDict)
        players = self.all()
        for player in players:
            if matrix.get(player.judge,{}).get(player.target, None):
                print "ERROR, already in matrix: ", player.judge, player.target, player.mu
            matrix[player.judge][player.target] = player.mu

        ordered_matrix = OrderedDict(sorted(matrix.items(), key=lambda x:x[0].user_id))
        players = matrix.keys()
        ## create a matrix of combined mu values represnted as costs (lower is better)
        munkres_matrix = []
        key_matrix = []
        for player1 in players:
            munkres_row = []
            key_matrix_row = []
            for player2 in players:
              mu_p1_p2 = ordered_matrix.get(player1, {}).get(player2, 0)
              mu_p2_p1 = ordered_matrix.get(player1, {}).get(player2, 0)
              munkres_row.append(1000 - mu_p1_p2 - mu_p2_p1)
              key_matrix_row.append((player1, player2))
            munkres_matrix.append(munkres_row)
            key_matrix.append(key_matrix_row)

        ## use Munkres to figure out the pairings to achieve highest combined mu values
        m = Munkres()
        munkres_indexes = m.compute(munkres_matrix)
        pairings = []
        ## save the results as Parings
        for row, column in munkres_indexes:
            print 'output: (%d, %d)' % (row, column)
            combined_mu = 1000 - munkres_matrix[row][column]
            player1 = key_matrix[row][column][0]
            player2 = key_matrix[row][column][1]
            new_pairing = Pairing(a=player1, b=player2, combined_mu=combined_mu)
            new_pairing.save()
            pairings.append(new_pairing)
            print '(%d, %d) -> %s %s, %s %s -> %d' % (row, column, player1.first_name, player1.last_name, player2.first_name, player2.last_name, combined_mu)
        return pairings
    
    def reorder_players_for_judge(self, judge):
        players_by_trueskill = self.filter(judge=judge).order_by('-mu')
        for index, player in enumerate(players_by_trueskill):
            player.trueskill_rank = index
        players_by_elo = self.filter(judge=judge).order_by('-elo')
        for index, player in enumerate(players_by_elo):
            player.trueskill_rank = index
            player.save()
        return players_by_trueskill

class Player(models.Model):
    judge = models.ForeignKey(Profile, related_name="player_judges", related_query_name="player_judge")
    target = models.ForeignKey(Profile, related_name="target", related_query_name="target")
    mu = models.FloatField(null=True, blank=True)
    sigma = models.FloatField(null=True, blank=True)
    elo = models.FloatField(null=True, blank=True)
    update_date = models.DateTimeField(auto_now=False, blank=True)
    trueskill_rank = models.PositiveIntegerField(null=True, blank=True)
    elo_rank = models.PositiveIntegerField(null=True, blank=True)

    objects = PlayerManager()

    def __unicode__(self):
        return "{0} {1}: {2} {3} has mu: {4}, sigma: {5}".format(self.judge.first_name, self.judge.last_name, self.target.first_name, self.target.last_name, self.mu, self.sigma)

class BattleManager(models.Manager):
    def create_battle(self, judge, leftProfile, rightProfile, randomizePosition=True):
        new_battle = Battle(left=leftProfile, right=rightProfile, judge=judge)
        new_battle.save()
        return new_battle

class Battle(models.Model):
    judge = models.ForeignKey(Profile, related_name="judges", related_query_name="judge", null=True, blank=True)
    left = models.ForeignKey(Profile, related_name="leftProfiles", related_query_name="leftProfile", null=True, blank=True)
    right = models.ForeignKey(Profile, related_name="rightProfiles", related_query_name="rightProfile", null=True, blank=True)
    winner = models.ForeignKey(Player, related_name="winners", related_query_name="winner", null=True, blank=True)
    loser = models.ForeignKey(Player, related_name="losers", related_query_name="loser", null=True, blank=True)
    
    left_gallery = models.ForeignKey(Gallery, related_name="left_battles", null=True, blank=True)
    right_gallery = models.ForeignKey(Gallery, related_name="right_battles", null=True, blank=True)
    data = HStoreField(null=True, blank=True)

    create_date = models.DateTimeField(auto_now=True)
    pick_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    expire_date = models.DateTimeField(auto_now=False, null=True, blank=True)

    # priority determines the order in which unfought battles should be displayed to the judge
    priority = models.FloatField(null=True, blank=True)

    objects = BattleManager()

    def __unicode__(self):
        return "{0} {1}: {2} {3} vs. {4} {5}".format(self.judge.first_name, self.judge.last_name, \
            self.left.first_name, self.left.last_name, \
            self.right.first_name, self.right.last_name)

    def pick(self, leftOrRight):
        if leftOrRight == 'left':
            self.winner = self.get_player(self.left)
            self.loser = self.get_player(self.right)
        if leftOrRight == 'right':
            self.winner = self.get_player(self.right)
            self.loser = self.get_player(self.left)
        self.pick_date = timezone.now()
        self.save()
        self.update_players()
        return self.winner

    def get_player(self, profile):
        date_now = timezone.now()
        playerQuery = Player.objects.filter(judge=self.judge, target=profile)
        if playerQuery.exists():
            player = playerQuery[0]
        else:
            newRating = Rating()
            player = Player(judge=self.judge, target=profile, update_date=date_now, mu=newRating.mu, sigma=newRating.sigma, elo=elo.INITIAL)
            player.save()
        return player

    def update_players(self):
        date_now = timezone.now()
        winnerTrueskillExistingRating = Rating(mu=self.winner.mu, sigma=self.winner.sigma)
        loserTrueskillExistingRating = Rating(mu=self.loser.mu, sigma=self.loser.sigma)

        winnerTrueskillUpdatedRating, loserTrueskillUpdatedRating = rate_1vs1(winnerTrueskillExistingRating, loserTrueskillExistingRating)
        elo_result = elo.rate_1vs1(self.winner.elo, self.loser.elo)

        self.winner.mu = winnerTrueskillUpdatedRating.mu
        self.winner.sigma = winnerTrueskillUpdatedRating.sigma
        self.winner.elo = elo_result[0]
        self.winner.update_date = timezone.now()
        self.winner.save()

        self.loser.mu = loserTrueskillUpdatedRating.mu
        self.loser.sigma = loserTrueskillUpdatedRating.sigma
        self.loser.elo = elo_result[1]
        self.loser.update_date = timezone.now()
        self.loser.save()

        return self.winner, self.loser
