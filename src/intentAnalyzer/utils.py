#-*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0,'../..')
import json
#from konlpy.tag import Twitter
from customKonlpy.ckonlpy.tag import Twitter
import jpype
import nltk
import time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
num_intent = 5

class Utils():
    def __init__(self):
        self.vocaList = []
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        self.twitter = Twitter()
        self.addCustumTag()
        time.sleep(2)

    def addCustumTag(self):
        customTag = json.load(open(os.path.join(BASE_DIR, './data/customtag.json'), 'r', encoding='UTF8'))
        for tag in customTag.keys():
            for word in customTag[tag]:
                self.twitter.add_custom_dictionary(word, tag)

    def tokenize(self, sentence):
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        posData = self.twitter.pos(sentence.strip())
        tokenized_sentense = []
        for tupple in posData:
            tokenized_sentense.append(tupple[0])
        return tokenized_sentense

    def tokenizeWithTag(self, sentence):
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        return self.twitter.pos(sentence.strip())


    def create_x_data(self, input_voca_list):
        bag = []
        for w in self.vocaList:
            bag.append(1) if w in input_voca_list else bag.append(0)
        return bag

    def load_voca(self):
        with open(os.path.join(BASE_DIR, './data/voca.voc'), 'r', encoding='utf-8') as vocab_file:
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
                output_empty = list([0] * num_intent)
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
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        self.twitter.add_dictionary('오늘', 'Date', force=True)
        self.twitter.add_dictionary('주가', 'Josa')
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        words = self.twitter.pos(sentence)
        parser = nltk.RegexpParser(grammar)
        chunks = parser.parse(words)
        for subtree in chunks.subtrees():
            print(subtree)
