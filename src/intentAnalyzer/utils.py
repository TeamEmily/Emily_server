#-*- coding: utf-8 -*-

import os
import json
#from konlpy.tag import Twitter
from ckonlpy.tag import Twitter
import nltk
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Utils():
    def __init__(self):
        self.vocaList = []

    def tokenize(self, sentence):
        twitter = Twitter()
        posData = twitter.pos(sentence.strip())
        print(posData)
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

    def make_chunk_bundle(self, sentence):
        grammar = """
        NP: {<N.*>*<Suffix>?}   # Noun phrase
        VP: {<V.*>*}            # Verb phrase
        AP: {<A.*>*}            # Adjective phrase
        """
        twitter = Twitter()
        twitter.add_dictionary('오늘', 'Date', force=True)
        twitter.add_dictionary('주가', 'Josa')
        words = twitter.pos(sentence)
        print(words)
        parser = nltk.RegexpParser(grammar)
        chunks = parser.parse(words)
        print("# Print whole tree")
        print(chunks)
        for subtree in chunks.subtrees():
            print(subtree)
            # if subtree.label()=='NP':
            #     print(' '.join((e[0] for e in list(subtree))))

def main():
    utils = Utils()
    utils.load_voca()
    utils.make_chunk_bundle("오늘의 주가정보에 대해 검색해줘")

if __name__ == "__main__":
    main()