from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
from epl.views import epl
from weather.views import WeatherReporter
import random

intentAnalyzer = IntentAnalyzer()
previous_intentNum = -1
previous_intent = ""
previous_params = {}
class getIntent(APIView):

    def get(self, request, format=None):
        global previous_intentNum
        global previous_intent
        global previous_params

        string = request.GET.get('str')
        intent, intent_num = intentAnalyzer.analyzeIntent(string)
        print("Analized intent is", intent_num)
        print("Previous Intent Number was:", previous_intentNum)
        print("Previous Parameter was:", previous_params)
        
        if(intent_num == -1):
            # return Response({"error": intent})
            if previous_intentNum == -1:
                return Response({"error": intent})
            else:
                intent_num = previous_intentNum
                intent = previous_intent
                
        params = intentAnalyzer.checkParameters(string, intent_num)
        print("Analized params is", params)
        
        if ("error" in params.keys()):
            # return Response({"error": params["error"]})
            if len(previous_params) == 0:
                return Response({"error": params["error"]})
            else:
                params = previous_params

        print("now Intent number is:", intent_num)
        print("and params is:", params)
        data, message = self.getResult(params, intent_num)
        previous_intent = intent
        previous_intentNum = intent_num
        previous_params = params
        return Response({"intent": intent, "data": data, "message":message})

    def getResult(self, params, intent):
        funcMap = {
            0: self.sayHello,
            1: WeatherReporter.reporter,
            2: epl.getRecord,
            3: epl.getPlayerInfo,
            4: epl.getGameRecord,
            5: self.twentyfifth_night,
            6: epl.getSchedule
        }
        data, message = funcMap[intent](params)
        return data, message

    def sayHello(self, params):
        n = random.randrange(0, 4)
        greeting = ["너도 안녕", "반가워~", "좋은 하루~", "또 와주었구나?"]
        message = ""
        return greeting[n], message

    def twentyfifth_night(self, params):
        greeting = "살아있다"
        message = ""
        return greeting, message