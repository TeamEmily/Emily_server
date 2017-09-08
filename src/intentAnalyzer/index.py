import os
import json
import tensorflow as tf
from data.processFormat import ProcessFormat
from data.trainingSet import TrainingSet
from controller.preprocessor import Preprocessor
from controller.trainingSetCreater import TrainingSetCreater
from controller.learning import Learning
from controller.predict import Predict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    inputJson = readFile()
    processFormat = ProcessFormat()
    preprocessor = Preprocessor(processFormat)
    preprocessor.preprocessing(inputJson)
    trainingSet = TrainingSet()
    trainingSetCreater = TrainingSetCreater(trainingSet)
    trainingSetCreater.create_trainingSet(processFormat)
    learning = Learning(trainingSet)
    learning.train()
    print(processFormat.classes)
    for step in range(10001):
        text = input("what do you want to say?")
        token_list = preprocessor.tokenize(text)
        print(token_list)
        x_data = trainingSetCreater.create_x_data(token_list, processFormat.words)
        print(x_data)
        predict = Predict([x_data])
        print(predict)

def readFile():
    with open(os.path.join(BASE_DIR, 'dummy.json'), 'r', encoding='UTF8') as dummy_data:
        return json.load(dummy_data)


if __name__ == '__main__':
    main()