from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from epl.models import Teamrecord, Players, Teams, Stats, Games
from epl.serializers import TeamRecordSerializer, PlayerRecordSerializer, TeamsSerializer, StatsSerializer, GamesSerializer, ScheduleSerializer
import datetime
from calendar import monthrange

class epl(APIView):
    def dateTimeTransformer(date, format=None):
        date = date.split('-')
        month = date[0]
        day = date[1]
        
        return month, day

    def getRecord(params, format=None):
        data = []
        for param in params["FC"]:
            if param == "리그":
                teamrecord = Teamrecord.objects.all()
                serializer = TeamRecordSerializer(teamrecord, many=True)
                return serializer.data
            else:
                obj = Teams.objects.filter(Q(team_nickname__icontains=param))
                teamserializer = TeamsSerializer(obj, many=True)
                teamname = teamserializer.data[0]["team_name"]
                teamrecord = Teamrecord.objects.filter(Q(pk=teamname))
                serializer = TeamRecordSerializer(teamrecord, many=True)
                team_pic = teamserializer.data[0]["team_pic"]
                serializer.data[0]["team_pic"] = team_pic
            data.extend(serializer.data)
        return data

    def getPlayerInfo(params, format=None):
        data = []
        
        players = params["Players"]
        for p in players:
            try:
                playerrecord = Players.objects.filter(pl_name__icontains=p)
            except Players.DoesNotExist:
                continue
            else:
                playedcount = Players.objects.filter(pl_name__icontains=p).count()
                playerserializer = PlayerRecordSerializer(playerrecord, many=True)
                player_id = playerserializer.data[0]["pl_id"]
                teamid = playerserializer.data[0]["team"]
                
                teamlist = Teams.objects.get(pk=teamid)
                teamserializer = TeamsSerializer(teamlist)
                playerserializer.data[0]["team_name"] = teamserializer.data["team_name"]
                
                del playerserializer.data[0]["team"]

                stats_data = Stats.objects.filter(fk_pl__exact=player_id)
                statsserializer = StatsSerializer(stats_data, many=True)
                goals, assists, shots, min_played, card_yellow, card_red, passes, touches, fouls, playedcount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
                    if int(i["min_played"]) > 0:
                        playedcount = playedcount + 1
                
                playerserializer.data[0]["goals"] = goals
                playerserializer.data[0]["assists"] = assists
                playerserializer.data[0]["shots"] = shots
                playerserializer.data[0]["min_played"] = min_played
                playerserializer.data[0]["card_yellow"] = card_yellow
                playerserializer.data[0]["card_red"] = card_red
                playerserializer.data[0]["passes"] = passes
                playerserializer.data[0]["touches"] = touches
                playerserializer.data[0]["fouls"] = fouls
                playerserializer.data[0]["played_games"] = playedcount
                
                data.extend(playerserializer.data)
            return data

    def getGameRecord(params, format=None):
        date = params["Date"][0].split('-')
        month = int(date[0])
        day = int(date[1])
        if len(params["FC"]) == 2:
            data = []
            team1 = params["FC"][0]
            team2 = params["FC"][1]
            t1 = Teams.objects.filter(Q(team_nickname__icontains=team1))
            t2 = Teams.objects.filter(Q(team_nickname__icontains=team2))
            t1serializer = TeamsSerializer(t1, many=True)
            t2serializer = TeamsSerializer(t2, many=True)
            t1_id = t1serializer.data[0]["team_id"]
            t2_id = t2serializer.data[0]["team_id"]
            teamname1 = t1serializer.data[0]["team_name"]
            teamname2 = t2serializer.data[0]["team_name"]
            home_pic = t1serializer.data[0]["team_pic"]
            away_pic = t2serializer.data[0]["team_pic"]
            if month == 0 and day == 0:
                d = datetime.datetime.today()
                obj = Games.objects.filter((Q(home_team=t1_id) | Q(away_team=t1_id)) & (Q(home_team=t2_id) | Q(away_team=t2_id)) & Q(game_date__lt=d)).order_by('-game_date')
                gameserializer = GamesSerializer(obj, many=True)
            elif month != 0 and day == 0:
                startd = datetime.date(2017, month, 1)
                endd = datetime.date(2017, month, monthrange(2017, month)[1])
                obj = obj = Games.objects.filter((Q(home_team=t1_id) | Q(away_team=t1_id)) & (Q(home_team=t2_id) | Q(away_team=t2_id)) & Q(game_date__range=(startd, endd)))
                gameserializer = GamesSerializer(obj, many=True)
            else:
                d = datetime.date(2017, month, day)
                obj = Games.objects.filter((Q(home_team=t1_id) | Q(away_team=t1_id)) & (Q(home_team=t2_id) | Q(away_team=t2_id)) & Q(game_date__startswith=d))
                gameserializer = GamesSerializer(obj, many=True)

            for i in gameserializer.data:
                home_id = i["home_team"]
                away_id = i["away_team"]
                homeObj = Teams.objects.filter(Q(team_id=home_id))
                awayObj = Teams.objects.filter(Q(team_id=away_id))
                h_serializer = TeamsSerializer(homeObj, many=True)
                aw_serializer = TeamsSerializer(awayObj, many=True)
                home_name = h_serializer.data[0]["team_name"]
                away_name = aw_serializer.data[0]["team_name"]
                home_pic = h_serializer.data[0]["team_pic"]
                away_pic = aw_serializer.data[0]["team_pic"]
                i["home_team"] = home_name
                i["away_team"] = away_name
                i["home_pic"] = home_pic
                i["away_pic"] = away_pic
                del i["game_id"]
                del i["round_id"]
            data.extend(gameserializer.data)
            return data

        elif len(params["FC"]) == 1:
            data = []
            team = params["FC"][0]
            t = Teams.objects.filter(Q(team_nickname__icontains=team))
            teamserializer = TeamsSerializer(t, many=True)
            t_id = teamserializer.data[0]["team_id"]

            if month == 0 and day == 0:
                d = datetime.datetime.today()
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__lt=d)).order_by('-game_date')
                gameserializer = GamesSerializer(obj, many=True)
            elif month != 0 and day == 0:
                startd = datetime.date(2017, month, 1)
                endd = datetime.date(2017, month, monthrange(2017, month)[1])
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__range=(startd, endd))).order_by('-game_date')
                gameserializer = GamesSerializer(obj, many=True)
            else:
                d = datetime.date(2017, month, day)
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__startswith=d))
                gameserializer = GamesSerializer(obj, many=True)

            for i in gameserializer.data:
                home_id = i["home_team"]
                away_id = i["away_team"]
                homeObj = Teams.objects.filter(Q(team_id=home_id))
                awayObj = Teams.objects.filter(Q(team_id=away_id))
                h_serializer = TeamsSerializer(homeObj, many=True)
                aw_serializer = TeamsSerializer(awayObj, many=True)
                home_name = h_serializer.data[0]["team_name"]
                away_name = aw_serializer.data[0]["team_name"]
                home_pic = h_serializer.data[0]["team_pic"]
                away_pic = aw_serializer.data[0]["team_pic"]
                i["home_team"] = home_name
                i["away_team"] = away_name
                i["home_pic"] = home_pic
                i["away_pic"] = away_pic
                del i["game_id"]
                del i["round_id"]
            data.extend(gameserializer.data)
            return data

    def getSchedule(params, format=None):
        date = params["Date"][0].split('-')
        month = int(date[0])
        day = int(date[1])

        data = []
        team = params["FC"][0]

        if team == "리그":
            t = Teams.objects.all()
            teamserializer = TeamsSerializer(t, many=True)
            d = datetime.datetime.today()
            obj = Games.objects.filter(Q(game_date__gt=d)).order_by('game_date')
            scdserializer = ScheduleSerializer(obj, many=True)
        else:
            t = Teams.objects.filter(Q(team_nickname__icontains=team))
            teamserializer = TeamsSerializer(t, many=True)
            t_id = teamserializer.data[0]["team_id"]
            
            if month == 0 and day == 0:
                d = datetime.datetime.today()
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__gt=d)).order_by('game_date')
                scdserializer = ScheduleSerializer(obj, many=True)
            elif month != 0 and day == 0:
                startd = datetime.date(2017, month, 1)
                endd = datetime.date(2017, month, monthrange(2017, month)[1])
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__range=(startd, endd))).order_by('game_date')
                scdserializer = ScheduleSerializer(obj, many=True)
            else:
                d = datetime.date(2017, month, day)
                obj = Games.objects.filter((Q(home_team=t_id) | Q(away_team=t_id)) & Q(game_date__startswith=d))
                scdserializer = ScheduleSerializer(obj, many=True)

        for i in scdserializer.data:
            home_id = i["home_team"]
            away_id = i["away_team"]
            homeObj = Teams.objects.filter(Q(team_id=home_id))
            awayObj = Teams.objects.filter(Q(team_id=away_id))
            h_serializer = TeamsSerializer(homeObj, many=True)
            aw_serializer = TeamsSerializer(awayObj, many=True)
            home_name = h_serializer.data[0]["team_name"]
            away_name = aw_serializer.data[0]["team_name"]
            home_pic = h_serializer.data[0]["team_pic"]
            away_pic = aw_serializer.data[0]["team_pic"]
            i["home_team"] = home_name
            i["away_team"] = away_name
            i["home_pic"] = home_pic
            i["away_pic"] = away_pic
        data.extend(scdserializer.data)
        return data