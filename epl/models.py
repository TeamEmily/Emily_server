# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Games(models.Model):
    game_id = models.IntegerField(primary_key=True)
    round_id = models.IntegerField()
    home_team = models.IntegerField()
    away_team = models.IntegerField()
    game_date = models.DateTimeField()
    game_referee = models.CharField(max_length=45, blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=45, blank=True, null=True)
    home_shoot = models.IntegerField(blank=True, null=True)
    away_shoot = models.IntegerField(blank=True, null=True)
    home_on_target = models.IntegerField(blank=True, null=True)
    away_on_target = models.IntegerField(blank=True, null=True)
    home_poss = models.IntegerField(blank=True, null=True)
    away_poss = models.IntegerField(blank=True, null=True)
    home_foul = models.IntegerField(blank=True, null=True)
    away_foul = models.IntegerField(blank=True, null=True)
    home_yellow = models.IntegerField(blank=True, null=True)
    home_red = models.IntegerField(blank=True, null=True)
    away_yellow = models.IntegerField(blank=True, null=True)
    away_red = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'
        unique_together = (('game_id', 'round_id', 'home_team', 'away_team'),)


class Players(models.Model):
    pl_id = models.IntegerField(primary_key=True)
    pl_name = models.CharField(max_length=45)
    pl_position = models.CharField(max_length=45)
    pl_num = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=45, blank=True, null=True)
    pl_pic = models.CharField(max_length=255, blank=True, null=True)
    pl_nic = models.CharField(max_length=255, blank=True, null=True)

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
    stat_id = models.AutoField(primary_key=True)
    fk_round = models.ForeignKey(Games, related_name='fk_round')
    fk_game = models.ForeignKey(Games, related_name='fk_game')
    fk_team = models.ForeignKey(Players, related_name='fk_team')
    fk_pl = models.ForeignKey(Players, related_name='fk_pl')
    status = models.CharField(max_length=45, blank=True, null=True)
    full_time = models.IntegerField(blank=True, null=True)
    min_played = models.IntegerField(blank=True, null=True)
    sub_with_id = models.IntegerField(blank=True, null=True)
    goals = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    card_yellow = models.IntegerField(blank=True, null=True)
    card_red = models.IntegerField(blank=True, null=True)
    shots = models.IntegerField(blank=True, null=True)
    passes = models.IntegerField(blank=True, null=True)
    touches = models.IntegerField(blank=True, null=True)
    saves = models.IntegerField(blank=True, null=True)
    clearance = models.IntegerField(blank=True, null=True)
    fouls = models.IntegerField(blank=True, null=True)
    ratings = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stats'
        unique_together = (('stat_id', 'fk_round', 'fk_game', 'fk_team', 'fk_pl'),)


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
    ranking = models.IntegerField(db_column='Ranking', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamrecord'


class Teams(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=45)
    team_stadium = models.CharField(max_length=45)
    team_manager = models.CharField(max_length=45, blank=True, null=True)
    team_nickname = models.CharField(max_length=45, blank=True, null=True)
    team_pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'
