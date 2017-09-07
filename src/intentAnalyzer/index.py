import os
import json
from data.processFormat import ProcessFormat
from data.trainingSet import TrainingSet
from controller.preprocessor import Preprocessor
from controller.trainingSetCreater import TrainingSetCreater
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    inputJson = readFile()
    processFormat = ProcessFormat()
    preprocessor = Preprocessor(processFormat)
    preprocessor.preprocessing(inputJson)
    trainingSet = TrainingSet()
    trainingSetCreater = TrainingSetCreater(trainingSet)
    trainingSetCreater.create_trainingSet(processFormat)

def readFile():
    with open(os.path.join(BASE_DIR, 'dummy.json'), 'r', encoding='UTF8') as dummy_data:
        return json.load(dummy_data)

if __name__ == '__main__':
    main()