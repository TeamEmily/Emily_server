import os
import json
import tensorflow as tf
# from data.processFormat import ProcessFormat
# from data.trainingSet import TrainingSet
# from controller.preprocessor import Preprocessor
# from controller.trainingSetCreater import TrainingSetCreater
# from controller.learning import Learning
# from controller.predict import Predict
from model import Model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class IntentAnalyzer():
    def readFile(self):
        with open(os.path.join(BASE_DIR, '/data/dummy.json'), 'r', encoding='UTF8') as dummy_data:
            return json.load(dummy_data)

    def analyzeIntent(self, str):
        print('Analyze')

def main():
    intentAnalyzer = IntentAnalyzer()

if __name__ == '__main__':
    main()