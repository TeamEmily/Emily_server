from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from epl.models import Teamrecord, Players, Teams, Stats, Games
from epl.serializers import TeamRecordSerializer, PlayerRecordSerializer, TeamsSerializer, StatsSerializer, GamesSerializer
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

    def getPlayerInfo(params, format=None):
        data = []
        
        players = params["Players"]
        for p in players:
            playerrecord = Players.objects.filter(pl_name__icontains=p)
            playerserializer = PlayerRecordSerializer(playerrecord, many=True)
            teamid = playerserializer.data[0]["team"]
            
            teamlist = Teams.objects.get(pk=teamid)
            teamserializer = TeamsSerializer(teamlist)
            playerserializer.data[0]["team_name"] = teamserializer.data["team_name"]
            
            del playerserializer.data[0]["team"]
            data.append(playerserializer.data)

            
        return data

    def getPlayerStat(params, format=None):
        print("HI IM AT getPlayerStat")
        data=[]

        players = params["Players"]
        print(players)
        for p in players:
            playerrecord = Players.objects.filter(pl_name__icontains=p)
            playerserializer = PlayerRecordSerializer(playerrecord, many=True)
            player_id = playerserializer.data[0]["pl_id"]
            print("Player_id: ", player_id)

            stats_data = Stats.objects.filter(fk_pl__exact=player_id)
            statsserializer = StatsSerializer(stats_data, many=True)
            print("At getPlayerStat: ", statsserializer.data)
            goals = 0
            assists = 0
            shots = 0
            for i in statsserializer.data:
                goals = goals + int(i["goals"])
                assists = assists + int(i["assists"])
                shots = shots + int(i["shots"])
            
            playerserializer.data[0]["goals"] = goals
            playerserializer.data[0]["assists"] = assists
            playerserializer.data[0]["shots"] = shots

            del playerserializer.data[0]["pl_id"]
            del playerserializer.data[0]["pl_position"]
            del playerserializer.data[0]["pl_num"]
            del playerserializer.data[0]["date_of_birth"]
            del playerserializer.data[0]["nationality"]
            del playerserializer.data[0]["team"]
            data.append(playerserializer.data)

        return data  

    def getGameRecord(params, format=None):
        data = []
        team1 = params["FC"][0]
        team2 = params["FC"][1]
        t1 = Teams.objects.filter(Q(team_name__startswith=team1))
        t2 = Teams.objects.filter(Q(team_name__startswith=team2))

        t1serializer = TeamsSerializer(t1, many=True)
        t2serializer = TeamsSerializer(t2, many=True)
        t1_id = t1serializer.data[0]["team_id"]
        t2_id = t2serializer.data[0]["team_id"]

        print("IM IN getGameRecord: ", t1_id, t2_id)
        pre_game_obj = Games.objects.filter(Q(home_team=t1_id) | Q(away_team=t1_id)).filter(Q(home_team=t2_id) | Q(away_team=t2_id))
        gameserializer = GamesSerializer(pre_game_obj, many=True)

        return gameserializer.data
