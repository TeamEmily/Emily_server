from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
from rest_framework.renderers import JSONRenderer
from epl.views import epl
from weather.views import WeatherReporter
import random

intentAnalyzer = IntentAnalyzer()

class getIntent(APIView):

    def get(self, request, format=None):
        string = request.GET.get('str')
        intent, intent_num = intentAnalyzer.analyzeIntent(string)
        if(intent_num == -1):
            return Response({"error": intent})
        params = intentAnalyzer.checkParameters(string, intent_num)
        if ("error" in params.keys()):
            return Response({"error": params["error"]})
        else:
            data = self.getResult(params, intent_num)
            return Response({"intent": intent, "data": data})

    def getResult(self, params, intent):
        funcMap = {
            0: self.sayHello,
            1: WeatherReporter.reporter,
            2: epl.getRecord,
            3: epl.getPlayerInfo,
            4: epl.getGameRecord,
            5: self.twentyfifth_night
        }
        return funcMap[intent](params)

    def sayHello(self, params):
        n = random.randrange(0, 4)
        greeting = ["너도 안녕", "반가워~", "좋은 하루~", "또 와주었구나?"]
        return greeting[n]

    def twentyfifth_night:
        greeting = "살아있다"
        return greeting