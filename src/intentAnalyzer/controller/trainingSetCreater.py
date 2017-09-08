class TrainingSetCreater:
    def __init__(self, trainingSet):
        self.trainingSet = trainingSet

    def create_trainingSet(self, data):
        output_empty = [0] * len(data.classes)

        for doc in data.documents:
            bag = self.create_x_data(doc[0], data.words)
            self.trainingSet.training.append(bag)

            output_row = list(output_empty)
            output_row[data.classes.index(doc[1])] = 1
            self.trainingSet.output.append(output_row)

    def create_x_data(self, token_list, words):
        bag = []
        for w in words:
            bag.append(1) if w in token_list else bag.append(0)
        return bag