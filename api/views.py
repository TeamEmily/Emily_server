from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
from rest_framework.renderers import JSONRenderer
from epl.models import Teamrecord
from epl.serializers import TeamRecordSerializer
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
        print(intent)
        funcMap = {
            0: self.sayHello,
            2: self.getRecord
        }
        return funcMap[intent](params)

    def getRecord(self, params, format=None):
        data = []
        for param in params["FC"]:
            if param == "리그":
                teamrecord = Teamrecord.objects.all()
                serializer = TeamRecordSerializer(teamrecord, many=True)
                return serializer.data
            else:
                teamrecord = Teamrecord.objects.get(pk=param)
                serializer = TeamRecordSerializer(teamrecord)
                print(serializer.data)
            data.append(serializer.data)
        return data

    def sayHello(self, params):
        n = random.randrange(0, 4)
        greeting = ["너도 안녕", "반가워~", "좋은 하루~", "또 와주었구나?"]
        return greeting[n]