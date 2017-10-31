from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer

class getIntent(APIView):
    def __init__(self):
        self.intentAnalyzer = IntentAnalyzer()

    def get(self, request, format=None):
        string = request.GET.get('str')
        intent, intent_num = self.intentAnalyzer.analyzeIntent(string)
        params = self.intentAnalyzer.checkParameters(string, intent_num)
        if ("error" in params.keys()):
            return Response({"error": params["error"]})
        else:
            return Response({"intent": intent, "params": params})
