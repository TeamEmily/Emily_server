from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from epl.models import Teamrecord
from epl.serializers import TeamRecordSerializer
# Create your views here.

class epl(APIView):
    
    def eplRecord(params):
        
        epl.getRecord(params)

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
                # print(serializer.data)
            data.append(serializer.data)
        return data


    def getRanking(params, format=None):
        data = []
        for param in params["FC"]:
            teamrecord = Teamrecord.objects.order_by('-totalpoints')
            serializer = TeamRecordSerializer(teamrecord, many=True)
            return serializer.data