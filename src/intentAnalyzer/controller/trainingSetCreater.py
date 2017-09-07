class TrainingSetCreater:
    def __init__(self, trainingSet):
        self.trainingSet = trainingSet

    def create_trainingSet(self, data):
        output_empty = [0] * len(data.classes)

        for doc in data.documents:
            bag = []
            pattern_words = doc[0]
            for w in data.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            self.trainingSet.training.append(bag)

            output_row = list(output_empty)
            output_row[data.classes.index(doc[1])] = 1
            self.trainingSet.output.append(output_row)