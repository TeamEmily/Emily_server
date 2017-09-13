import os
import json
import tensorflow as tf
from trainModel import Model
from utils import Utils

def analyzeIntent(str):
    model = Model()
    utils = Utils()
    utils.load_voca()
    tokenized_str = utils.tokenize(str)
    x_data = utils.create_x_data(tokenized_str)
    print(x_data)
    print(model.predict([x_data]))


def main():
    analyzeIntent('안녕하세여 김유영이라고 해여')

if __name__ == '__main__':
    main()