import os
import json
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
            return "Sorry We can't find intent"
        else:
            return self.intentData[str(intent_index)]["name"]

def main():
    intentAnalyzer = IntentAnalyzer()
    for w in range (10):
        sentense = input("str: ")
        print(intentAnalyzer.analyzeIntent(sentense))

if __name__ == '__main__':
    main()