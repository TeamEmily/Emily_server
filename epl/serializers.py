from django.forms import widgets
from rest_framework import serializers
from epl.models import Teams, Stats, Teamrecord, Players


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('team_id', 'team_name', 'team_stadium', 'team_manager', 'team_nickname')

class TeamRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teamrecord
        fields = ('teamname', 'totalpoints', 'gamesplayed', 'winnum', 'losenum', 'drawnum', 'goalscored', 'goalconceded', 'goaldifference')