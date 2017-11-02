from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
from rest_framework.renderers import JSONRenderer
from epl.models import Teamrecord
from epl.serializers import TeamRecordSerializer

intentAnalyzer = IntentAnalyzer()

class getIntent(APIView):

    def get(self, request, format=None):
        teamrecord = Teamrecord.objects.all()
        serializer = TeamRecordSerializer(teamrecord, many=True)
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
            2: self.getRecord(params)
        }
        return funcMap.get(intent)

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