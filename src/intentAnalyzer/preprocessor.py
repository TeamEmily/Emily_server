import os
import json
from konlpy.tag import Twitter
import trainingSetCreater

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
words = []
classes = []
documents = []

def main():
    with open(os.path.join(BASE_DIR, 'dummy.json'), 'r', encoding='UTF8') as dummy_data:
        data = json.load(dummy_data)
        setData(data)
        removeDuplication()
        trainingSetCreater.create_trainingSet(words, classes, documents)

def removeDuplication():
    global classes
    global words
    words = list(set(words))
    classes = list(set(classes))
    print(words)
    print(classes)

def setData(data):
    for obj in data['training_data']:
        tokenized_sentense = tokenize(obj['sentence'])
        for tupple in tokenized_sentense:
            words.append(tupple[0])
        documents.append((words, obj['class']))
        classes.append(obj['class'])

def tokenize(str):
    twitter = Twitter()
    return twitter.pos(str.strip())

if __name__ == '__main__':
    main()
