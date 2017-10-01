from rest_framework.views import APIView
from rest_framework.response import Response
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer

class getIntent(APIView):
    def __init__(self):
        self.intentAnalyzer = IntentAnalyzer()

    def get(self, request, string, format=None):
        return Response(self.intentAnalyzer.analyzeIntent(string))