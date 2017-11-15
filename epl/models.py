# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    round = models.ForeignKey('Round', models.DO_NOTHING)
    home_team = models.CharField(max_length=45)
    away_team = models.CharField(max_length=45)
    game_date = models.CharField(max_length=45, blank=True, null=True)
    game_referee = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'
        unique_together = (('game_id', 'round', 'home_team', 'away_team'),)


class Players(models.Model):
    pl_id = models.IntegerField(primary_key=True)
    pl_name = models.CharField(max_length=45)
    pl_position = models.CharField(max_length=45)
    pl_num = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'
        unique_together = (('pl_id', 'team'),)


class Round(models.Model):
    round_id = models.IntegerField(primary_key=True)
    round_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'round'


class Stats(models.Model):
    stat_id = models.IntegerField(primary_key=True)
    fk_pl = models.ForeignKey(Players, related_name='fk_pl')
    fk_game = models.ForeignKey(Game, related_name='fk_game')
    status = models.CharField(max_length=45, blank=True, null=True)
    min_played = models.CharField(max_length=45, blank=True, null=True)
    goals = models.CharField(max_length=45, blank=True, null=True)
    assists = models.CharField(max_length=45, blank=True, null=True)
    card_yellow = models.CharField(max_length=45, blank=True, null=True)
    card_red = models.CharField(max_length=45, blank=True, null=True)
    fk_round = models.ForeignKey(Game, related_name='fk_round')
    fk_team = models.ForeignKey(Players, related_name='fk_team')

    class Meta:
        managed = False
        db_table = 'stats'
        unique_together = (('stat_id', 'fk_pl', 'fk_game', 'fk_round', 'fk_team'),)


class Teamrecord(models.Model):
    teamname = models.CharField(db_column='Teamname', primary_key=True, max_length=20)  # Field name made lowercase.
    totalpoints = models.IntegerField(db_column='TotalPoints')  # Field name made lowercase.
    gamesplayed = models.IntegerField(db_column='GamesPlayed')  # Field name made lowercase.
    winnum = models.IntegerField(db_column='Winnum')  # Field name made lowercase.
    losenum = models.IntegerField(db_column='Losenum')  # Field name made lowercase.
    drawnum = models.IntegerField(db_column='Drawnum')  # Field name made lowercase.
    goalscored = models.IntegerField(db_column='GoalScored')  # Field name made lowercase.
    goalconceded = models.IntegerField(db_column='GoalConceded')  # Field name made lowercase.
    goaldifference = models.IntegerField(db_column='GoalDifference')  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking')
    class Meta:
        managed = False
        db_table = 'teamrecord'


class Teams(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=45)
    team_stadium = models.CharField(max_length=45)
    team_manager = models.CharField(max_length=45, blank=True, null=True)
    team_nickname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'
