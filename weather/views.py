from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from weather.models import Weather  
from weather.serializers import WeatherSerializer
import datetime
class WeatherReporter(APIView):

    def reporter(params):
        if params["Date"] == ["00-00"]:
            message = "we can't find Date value"
            return params, message 
        try:
            params["City"]
        except KeyError:
            message = "we can't find City value"
            return params, message
        
        date = params["Date"][0]
        city = params["City"][0]
        if date == "오늘":
            data = WeatherReporter.WeatherToday(city)
        elif date == "내일":
            data = WeatherReporter.WeatherTomorrow(city)

        message = ":D"
        return data, message

    def WeatherToday(city):
        date = datetime.date.today()
        obj = Weather.objects.filter(city_name__icontains=city).filter(current_date=date)
        data = WeatherSerializer(obj, many=True)
        return data.data

    def WeatherTomorrow(city):
        date = datetime.date.today() + datetime.timedelta(1)
        obj = Weather.objects.filter(city_name__icontains=city).filter(current_date=date)
        data = WeatherSerializer(obj, many=True)
        return data.data
