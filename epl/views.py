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
            player_id = playerserializer.data[0]["pl_id"]
            teamid = playerserializer.data[0]["team"]
            
            teamlist = Teams.objects.get(pk=teamid)
            teamserializer = TeamsSerializer(teamlist)
            playerserializer.data[0]["team_name"] = teamserializer.data["team_name"]
            
            del playerserializer.data[0]["team"]

            stats_data = Stats.objects.filter(fk_pl__exact=player_id)
            statsserializer = StatsSerializer(stats_data, many=True)
            print("At getPlayerStat: ", statsserializer.data)
            goals = 0
            assists = 0
            shots = 0
            min_played = 0
            card_yellow = 0
            card_red = 0
            passes = 0
            touches = 0
            fouls = 0
            for i in statsserializer.data:
                goals = goals + int(i["goals"])
                assists = assists + int(i["assists"])
                shots = shots + int(i["shots"])
                min_played = min_played + int(i["min_played"])
                card_yellow = card_yellow + int(i["card_yellow"])
                card_red = card_red + int(i["card_red"])
                passes = passes + int(i["passes"])
                touches = touches + int(i["touches"])
                fouls = fouls + int(i["fouls"]) 
            
            playerserializer.data[0]["goals"] = goals
            playerserializer.data[0]["assists"] = assists
            playerserializer.data[0]["shots"] = shots
            playerserializer.data[0]["min_played"] = min_played
            playerserializer.data[0]["card_yellow"] = card_yellow
            playerserializer.data[0]["card_red"] = card_red
            playerserializer.data[0]["passes"] = passes
            playerserializer.data[0]["touches"] = touches
            playerserializer.data[0]["fouls"] = fouls
            data.append(playerserializer.data)
            
        return data

    def getGameRecord(params, format=None):
        # if len(params["FC"]) != 2:
        #     data = {}
        #     data["error"] = "Number of parameter for getGameRecord must be 2"
        #     return data
        
        if len(params["FC"]) == 2:
            data = []
            team1 = params["FC"][0]
            team2 = params["FC"][1]
            t1 = Teams.objects.filter(Q(team_name__startswith=team1))
            t2 = Teams.objects.filter(Q(team_name__startswith=team2))

            t1serializer = TeamsSerializer(t1, many=True)
            t2serializer = TeamsSerializer(t2, many=True)
            t1_id = t1serializer.data[0]["team_id"]
            t2_id = t2serializer.data[0]["team_id"]
            teamname1 = t1serializer.data[0]["team_name"]
            teamname2 = t2serializer.data[0]["team_name"]

            pre_game_obj = Games.objects.filter(Q(home_team=t1_id) | Q(away_team=t1_id)).filter(Q(home_team=t2_id) | Q(away_team=t2_id))
            gameserializer = GamesSerializer(pre_game_obj, many=True)

            del gameserializer.data[0]["game_id"]
            del gameserializer.data[0]["home_team"]
            del gameserializer.data[0]["away_team"]
            gameserializer.data[0]["home_team"] = teamname1
            gameserializer.data[0]["away_team"] = teamname2

            return gameserializer.data
        elif len(params["FC"]) == 1:
            data = []
            team = params["FC"][0]
            t = Teams.objects.filter(Q(team_name__startswith=team))
            teamserializer = TeamsSerializer(t, many=True)
            t_id = teamserializer.data[0]["team_id"]
            teamname = teamserializer.data[0]["team_name"]

            pre_game_obj = Games.objects.filter(Q(home_team=t_id) | Q(away_team=t_id)).order_by('-game_date')
            gameserializer = GamesSerializer(pre_game_obj, many=True)

            
            return gameserializer.data
