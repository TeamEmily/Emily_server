# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    home_team = models.CharField(max_length=45)
    away_team = models.CharField(max_length=45)
    round = models.ForeignKey('Round', models.DO_NOTHING)
    game_date = models.CharField(max_length=45, blank=True, null=True)
    game_referee = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'
        unique_together = (('game_id', 'home_team', 'away_team', 'round'),)


class Players(models.Model):
    pl_id = models.IntegerField(primary_key=True)
    pl_name = models.CharField(max_length=45)
    pl_position = models.CharField(max_length=45)
    pl_num = models.CharField(max_length=45)
    team = models.ForeignKey('Teams', models.DO_NOTHING)

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
    fk_pl = models.ForeignKey(Players, models.DO_NOTHING)
    fk_game = models.ForeignKey(Game, models.DO_NOTHING)
    status = models.CharField(max_length=45, blank=True, null=True)
    min_played = models.CharField(max_length=45, blank=True, null=True)
    goals = models.CharField(max_length=45, blank=True, null=True)
    assists = models.CharField(max_length=45, blank=True, null=True)
    card_yellow = models.CharField(max_length=45, blank=True, null=True)
    card_red = models.CharField(max_length=45, blank=True, null=True)
    fk_round = models.ForeignKey(Game, models.DO_NOTHING)
    fk_team = models.ForeignKey(Players, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stats'
        unique_together = (('stat_id', 'fk_pl', 'fk_game', 'fk_round', 'fk_team'),)


class Teamrecord(models.Model):
    teamname = models.CharField(db_column='Teamname', primary_key=True, max_length=20)  # Field name made lowercase.
    winscore = models.IntegerField(db_column='Winscore')  # Field name made lowercase.
    playedgames = models.IntegerField(db_column='Playedgames')  # Field name made lowercase.
    winnum = models.IntegerField(db_column='Winnum')  # Field name made lowercase.
    losenum = models.IntegerField(db_column='Losenum')  # Field name made lowercase.
    drawnum = models.IntegerField(db_column='Drawnum')  # Field name made lowercase.
    goalscore = models.IntegerField(db_column='Goalscore')  # Field name made lowercase.
    losepoint = models.IntegerField(db_column='Losepoint')  # Field name made lowercase.
    difgoallose = models.IntegerField(db_column='Difgoallose')  # Field name made lowercase.

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
