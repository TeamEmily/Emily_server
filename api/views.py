from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
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
            return Response({"intent": intent, "params": params})
