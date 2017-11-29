from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from epl.models import Teamrecord, Players, Teams, Stats, Games
from epl.serializers import TeamRecordSerializer, PlayerRecordSerializer, TeamsSerializer, StatsSerializer, GamesSerializer, ScheduleSerializer, PerformanceSerializer
import datetime
import random
from calendar import monthrange

class epl(APIView):
    def getRecord(params, format=None):
        data = []
        for param in params["FC"]:
            if param == "리그":
                teamrecord = Teamrecord.objects.all()
                serializer = TeamRecordSerializer(teamrecord, many=True)
                message = "20개 팀의 모든 정보입니다! :D"
                return serializer.data, message
            else:
                obj = Teams.objects.filter(Q(team_nickname__icontains=param))
                teamserializer = TeamsSerializer(obj, many=True)
                teamname = teamserializer.data[0]["team_name"]
                teamrecord = Teamrecord.objects.filter(Q(pk=teamname))
                serializer = TeamRecordSerializer(teamrecord, many=True)
                team_pic = teamserializer.data[0]["team_pic"]
                serializer.data[0]["team_pic"] = team_pic
            data.extend(serializer.data)
        
        message = ["검색하신 팀의 향후 일정이 궁금하세요? '향후 일정도 알려줘!' 라고 하시면 알려드릴께요!",
            "검색하신 팀의 최근 경기 결과가 궁금하시면, '최근 경기 결과가 어떻게 돼?' 라고 쳐보세요 :D",
            "다른 팀의 승점도 궁금하신가요? '[팀 이름] 도 부탁해!', 라고 말씀하세요!"]
        n = random.randrange(0, len(message))
        return data, message[n]

    def getPlayerInfo(params, format=None):
        data = []
        
        players = params["Players"]
        for p in players:
            try:
                playerrecord = Players.objects.filter(pl_nic__icontains=p)
            except Players.DoesNotExist:
                continue
            else:
                playerserializer = PlayerRecordSerializer(playerrecord, many=True)
                player_name = playerserializer.data[0]["pl_name"]
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
            message = ["다른 선수의 성적도 궁금하시면 '[선수 이름] 은? 라고 해주세요! 알려드리겠습니다 :D",
            "[선수 이름] 도 부탁해! 라고 하시면 그 선수 성적도 보여 드릴께요! XD"]
            n = random.randrange(0, len(message))
            return data, message[n]

    def getGameRecord(params, format=None):
        try:
            params["Date"]
        except KeyError:
            params["Date"] = ["00-00"]

        date = params["Date"][0].split('-')
        print("at getGameRecord", date)
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
            message = ["검색하신 팀의 향후 일정도 궁금하세요? '향후 일정도 알려줘!' 라고 하시면 알려드릴께요!",
            "검색하신 팀의 현재 순위가 궁금하시면, '순위도 알려줘!' 라고 쳐보세요 :D",
            "다른 팀의 경기 결과도 궁금하신가요? '[팀 이름] 은?', 라고 말씀하세요!"]
            n = random.randrange(0, len(message))
            return data, message[n]

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
            
            message = ["검색하신 팀의 향후 일정도 궁금하세요? '향후 일정도 알려줘!' 라고 하시면 알려드릴께요!",
            "검색하신 팀의 현재 순위가 궁금하시면, '순위도 알려줘!' 라고 쳐보세요 :D",
            "다른 팀의 경기 결과도 궁금하신가요? '[팀 이름] 은?', 라고 말씀하세요!"]
            n = random.randrange(0, len(message))
            return data, message[n]

    def getSchedule(params, format=None):
        try:
            params["Date"]
        except KeyError:
            params["Date"] = ["00-00"]
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
            for team in params["FC"]:
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
        message = ["이 팀의 현재 승점이 궁금하시면 '승점은 몇 점이야?' 라고 해주세요! 알려드릴께요 :D",
        "다른 팀의 일정도 알고 싶으시면 '[팀 이름] 은? 라고 물어보세요! 안내하겟읍니다 ( _ _)",
        "'최근 경기 어떻게 됬어?' 라고 물어보시면 경기 결과를 알려드리겠습니다 :)"]
        n = random.randrange(0, len(message))
        return data, message[n]
    
    def playerPerformance(params, format=None):
        # date = params["Date"][0].split('-')
        # month = int(date[0])
        # day = int(date[1])
        # data = []
        players = params["Players"]
        for p in players:
            playerObj = Players.objects.filter(Q(pl_nic__icontains=p))
            playerserializer = PlayerRecordSerializer(playerObj, many=True)
            player_id = playerserializer.data[0]["pl_id"]
            player_name = playerserializer.data[0]["pl_name"]
            teamid = playerserializer.data[0]["team"]
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

                obj = Games.objects.filter((Q(home_team=t1_id) | Q(away_team=t1_id)) & (Q(home_team=t2_id) | Q(away_team=t2_id)))
                gameserializer = GamesSerializer(obj, many=True)
        

            elif len(params["FC"]) == 1:
                data = []
                team = params["FC"][0]
                t = Teams.objects.filter(Q(team_nickname__icontains=team))
                teamserializer = TeamsSerializer(t, many=True)
                t_id = teamserializer.data[0]["team_id"]
                obj = Games.objects.filter(Q(home_team=t_id) | Q(away_team=t_id))
                gameserializer = GamesSerializer(obj, many=True)
                
        #     if month == 0 and day == 0:
        #         d = datetime.datetime.today()
        #         gameObj = Games.objects.filter((Q(home_team=teamid) | Q(away_team=teamid)) & Q(game_date__lt=d)).order_by('-game_date')
        #         gameserializer = GamesSerializer(gameObj, many=True)
        #     elif month != 0 and day == 0:
        #         startd = datetime.date(2017, month, 1)
        #         endd = datetime.date(2017, month, monthrange(2017, month)[1])
        #         gameObj = Games.objects.filter((Q(home_team=teamid) | Q(away_team=teamid)) & Q(game_date__range=(startd, endd))).order_by('-game_date')
        #         gameserializer = GamesSerializer(gameObj, many=True)
        #     else:
        #         d = datetime.date(2017, month, day)
        #         gameObj = Games.objects.filter((Q(home_team=teamid) | Q(away_team=teamid)) & Q(game_date__startswith=d))
        #         gameserializer = GamesSerializer(gameObj, many=True)

            for i in gameserializer.data:
                gameid = i["game_id"]
                gamedate = i["game_date"]
                statsObj = Stats.objects.filter(Q(fk_game=gameid) & Q(fk_pl=player_id))
                sSerializer = PerformanceSerializer(statsObj, many=True)
                if len(sSerializer.data) == 0:
                    continue
                if sSerializer.data[0]["sub_with_id"] != None:
                    subObj = Players.objects.filter(Q(pl_id=sSerializer.data[0]["sub_with_id"]))
                    subserializer = PlayerRecordSerializer(subObj, many=True)
                    sSerializer.data[0]["sub_with_id"] = subserializer.data[0]["pl_name"]
                sSerializer.data[0]["game_date"]=gamedate
                sSerializer.data[0]["pl_name"]=player_name
                del sSerializer.data[0]["fk_game"]
                del sSerializer.data[0]["fk_team"]
                del sSerializer.data[0]["fk_pl"]
                data.extend(sSerializer.data)
        
        message = ["이 경기의 다른 선수의 퍼포먼스도 궁금하시다면 [선수 이름] 도 알려줘! 라고 말해주세요 :D",
        "'성적 종합해서 보여줘' 라고 말씀하시면 이번 시즌 이 선수의 종합 스텟을 보여드릴게요 XD"]
        n = random.randrange(0, len(message))
        return data, message[n]