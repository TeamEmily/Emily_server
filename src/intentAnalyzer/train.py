from utils import Utils
from trainModel import Model

def train():
    utils = Utils()
    utils.load_voca()
    x_data, y_data = utils.build_training_data()
    model = Model()
    model.train(x_data, y_data)

def main():
    train()

if __name__ == "__main__":
    main()