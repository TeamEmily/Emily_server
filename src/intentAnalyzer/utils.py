#-*- coding: utf-8 -*-

import os
import json
from konlpy.tag import Twitter
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Utils():
    def __init__(self):
        self.vocaList = []

    def tokenize(self, str):
        twitter = Twitter()
        posData = twitter.pos(str.strip())
        tokenized_sentense = []
        for tupple in posData:
            tokenized_sentense.append(tupple[0])
        return tokenized_sentense

    def create_x_data(self, input_voca_list):
        bag = []
        for w in self.vocaList:
            bag.append(1) if w in input_voca_list else bag.append(0)
        return bag

    def load_voca(self):
        with open('./data/voca.voc', 'r', encoding='utf-8') as vocab_file:
            for line in vocab_file:
                self.vocaList.append(line.strip())

    def build_voca(self):
        with open(os.path.join(BASE_DIR, './data/dummy.json'), 'r', encoding='UTF8') as dummy_data:
            data = json.load(dummy_data)
            for obj in data["training_data"]:
                sentense = obj["sentence"]
                tokenized_voca = self.tokenize(sentense)
                self.vocaList.extend(tokenized_voca)
        self.vocaList = list(set(self.vocaList))
        with open('./data/voca.voc', 'w', encoding="utf-8") as vocab_file:
            for v in self.vocaList:
                print(v.encode('utf-8'))
                vocab_file.write(v + '\n')

    def build_training_data(self):
        x_data = []
        y_data = []
        with open(os.path.join(BASE_DIR, './data/dummy.json'), 'r', encoding='UTF8') as dummy_data:
            data = json.load(dummy_data)
            for obj in data["training_data"]:
                output_empty = list([0] * 3)
                sentense = obj["sentence"]
                intent = obj["intent"]
                tokenized_voca = self.tokenize(sentense)
                x_data.append(self.create_x_data(tokenized_voca))
                output_empty[intent] = 1
                y_data.append(output_empty)
        return x_data, y_data

def main():
    utils = Utils()
    utils.load_voca()
    x_data, y_data = utils.build_training_data()
    print(x_data)
    print(y_data)

if __name__ == "__main__":
    main()