from django.forms import widgets
from rest_framework import serializers
from epl.models import Teams, Stats, Teamrecord, Players, Games


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'

class TeamRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teamrecord
        fields = '__all__'

class PlayerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = '__all__'

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ('home_team', 'away_team', 'game_date')