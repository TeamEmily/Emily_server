from rest_framework import serializers
from weather.models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('city_name', 'morn_weather', 'morn_temperature', 'morn_rainfall', 'noon_weather', 'noon_temperature', 'noon_rainfall', 'current_date')