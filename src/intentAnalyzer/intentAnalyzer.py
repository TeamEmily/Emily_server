import os
import json
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from src.intentAnalyzer.trainModel import Model
from src.intentAnalyzer.utils import Utils

class IntentAnalyzer():
    def __init__(self):
        intent_json = open(os.path.join(BASE_DIR, './data/intent.json'), 'r', encoding='UTF8')
        self.intentData = json.load(intent_json)
        self.model = Model()
        self.utils = Utils()
        self.utils.load_voca()


    def analyzeIntent(self, sentense):
        tokenized_str = self.utils.tokenize(sentense)
        x_data = self.utils.create_x_data(tokenized_str)
        intent_index = self.model.predict([x_data])
        if intent_index == -1:
            return "Sorry We can't find intent", -1
        else:
            return self.intentData[str(intent_index)]["name"], intent_index

    def checkParameters(self, sentence, intent):
        response = {}
        params = self.intentData[str(intent)]["params"]
        if "Date" in params:
            sentence, outputStr = self.getDate(sentence)
            if (len(outputStr) > 0):
                response["Date"] = [outputStr]
        tokenized_sentence = self.utils.tokenizeWithTag(sentence)
        for param in params:
            p = [idx for idx, val in enumerate(tokenized_sentence) if param == val[1]]
            if len(p) == 0:
                if len(response[param]) > 0:
                    continue
                response["error"] = "we cant find " + param + " " + "value"
            else:
                response[param] = [tokenized_sentence[i][0] for i in p]
        return response

    def getDate(self, sentence):
        regex = re.compile('[0-1]?[0-9]월[\s]?([0-3]?[0-9]일)?')
        if regex.search(sentence) == None:
            outputStr = '00-00'
            return sentence, outputStr
        matchingStr = regex.search(sentence).group()
        print("at GetDate:", regex.search(sentence))
        outputStr = ''
        if len(matchingStr) > 0:
            sentence = sentence.replace(matchingStr, '')
            regex = re.compile('[0-9][0-9]*')
            matchingStr = regex.findall(matchingStr)
            outputStr += matchingStr[0] + '-'
            if (len(matchingStr) > 1):
                outputStr += matchingStr[1]
            else:
                outputStr += '0'
        return sentence, outputStr
