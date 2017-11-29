from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from src.intentAnalyzer.intentAnalyzer import IntentAnalyzer
from epl.views import epl
from weather.views import WeatherReporter
import random
import datetime
intentAnalyzer = IntentAnalyzer()
previous_intentNum = None
previous_intent = ""
previous_params = {}
class getIntent(APIView):

    def get(self, request, format=None):
        global previous_intentNum
        global previous_intent
        global previous_params

        string = request.GET.get('str')
        intent, intent_num = intentAnalyzer.analyzeIntent(string)
        print("Analized intent is", intent_num)
        print("Previous Intent Number was:", previous_intentNum)
        print("Previous Parameter was:", previous_params)
        temp_intent, temp_intent_num = intent, intent_num
        flag = False
        if(intent_num == None):
            # return Response({"error": intent})
            if previous_intentNum == None:
                return Response({"intent": "greeting", "message":"죄송해요ㅠ 뭘 원하시는지 알 수가 없네요..."})
            else:
                intent_num = previous_intentNum
                intent = previous_intent
                flag = True

        params = intentAnalyzer.checkParameters(string, intent_num)

        #### params = {"FC": None, "Players":"케인"}
        flag2 = False
        for param in params:
            if params[param] != None:
                if param != "Date":
                    flag2 = True
        if flag and not flag2:
            return Response({"intent": "greeting", "message":"죄송해요ㅠ 뭘 원하시는지 알 수가 없네요..."})
        for param in params:
            if params.get(param) == None:
                try:
                    previous_params[param]
                except KeyError: # {"Date", "FC"}
                    return Response({"intent": "greeting", "message": "죄송해요ㅠ "+param+"이(가) 뭔지 몰라서 알려드릴수 없어요. :("})
                else:
                    if previous_params[param] == None:
                        return Response({"intent": "greeting", "message": "죄송해요ㅠ "+param+"이(가) 뭔지 몰라서 알려드릴수 없어요. :("})
                    else:
                        params[param] = previous_params[param]

            
        # if ("error" in params.keys()):
        #     # return Response({"error": params["error"]})
        #     if len(previous_params) == 0:
        #         return Response({"error": params["error"]})
        #     else:
        #         print("im here")
        #         previous_params.update(params)
        #         params = previous_params
        #         del params['error']

        print("now Intent number is:", intent_num)
        print("and params is:", params)
        data, message = self.getResult(params, intent_num)
        previous_intent = intent
        previous_intentNum = intent_num
        previous_params = params
        return Response({"intent": intent, "data": data, "message":message})

    def getResult(self, params, intent):
        funcMap = {
            0: self.twentyfifth_night,
            1: self.sayHello,
            2: self.hungry,
            3: WeatherReporter.reporter,
            4: epl.getTeamRecord,
            5: epl.getPlayerInfo,
            6: epl.getGameRecord,
            7: epl.getSchedule,
            8: epl.playerPerformance,
            9: self.badWord,
            10: self.tryExit
        }
        data, message = funcMap[intent](params)
        return data, message

    def sayHello(self, params):
        n = random.randrange(0, 4)
        greeting = ["너도 안녕", "반가워~", "좋은 하루~", "또 와주었구나?"]
        message = greeting[n]
        return greeting[n], message

    def twentyfifth_night(self, params):
        greeting = "살아있다"
        message = "살아있다"
        return greeting, message

    def hungry(self, params):
        now = datetime.datetime.now()
        nowP = now.strftime('%p')

        midnight_start = now.replace(hour=0, minute=0)
        midnight_end = now.replace(hour=6, minute=0)
        morning_end = now.replace(hour=10, minute=0)
        noon_start = now.replace(hour=12, minute=0)
        noon_end = now.replace(hour=14, minute=0)
        dinner_start = now.replace(hour=18, minute=0)
        dinner_end = now.replace(hour=21, minute=0)
        message = ""
        if (midnight_start < now <= midnight_end):
            message = "아직 안자고 뭐하세요-_-z 님도 개발자세요? 야식은 죄악이에요 XD"
        elif (midnight_end < now <= morning_end):
            message = "아침 먹을 시간이긴 하네요! 저는 아침 잘 안 먹어서 제끼는데 님은 꼭 챙겨드세요 :D"
        elif (morning_end < now <= noon_start):
            messgae = "아침 아직 안드셨어요? 님도 저처럼 아침 싫어하는군요!"
        elif (noon_start < now <= noon_end):
            message = "저도 아침 안먹어서 죽겠네요 'ㅁ' 같이 학식 드쉴?"
        elif (noon_end < now <= dinner_start):
            message = "점심도 안 먹고 뭐하셨어요! 또 지금 먹고 저녁 늦게 먹을라고 그러죠?"
        elif (dinner_start < now <= dinner_end):
            message = "저녁엔 치킨이죠!"
        elif (dinner_end < now <= midnight_start):
            message = "지금 밥 먹으면 살쪄요^^ 참아요ㅎ"
        greeting = message
        return greeting, message

    def badWord(self, params):
        message = ["죄송해요. 잘 알아들을 수 있도록 노력할께요ㅠㅠ",
        "욕하지 마세요ㅠㅠ 저도 최선을 다하고 있답니다..",
        "엉엉ㅠㅠㅠ",
        ".... 죄송합니다."]
        n = random.randrange(0, len(message))
        greeting = message[n]
        return greeting, message[n]

    def tryExit(self, params):
        message = "정말 나가시겠어요?"
        greeting = message
        return greeting, message