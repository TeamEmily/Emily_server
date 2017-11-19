from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from epl.models import Teamrecord, Players
from epl.serializers import TeamRecordSerializer, PlayerRecordSerializer
# Create your views here.

class epl(APIView):
    def getRecord(params, format=None):
        data = []
        for param in params["FC"]:
            if param == "리그":
                teamrecord = Teamrecord.objects.all()
                serializer = TeamRecordSerializer(teamrecord, many=True)
                return serializer.data
            else:
                teamrecord = Teamrecord.objects.get(pk=param)
                serializer = TeamRecordSerializer(teamrecord)
            data.append(serializer.data)
        return data

    def getPlayerRecord(params, format=None):
        
        players = params["Players"][0]
        print("getPlayerRecord: ", players)
        playerrecord = Players.objects.filter(pl_name__icontains=players)
        serializer = PlayerRecordSerializer(playerrecord, many=True)
        return serializer.data