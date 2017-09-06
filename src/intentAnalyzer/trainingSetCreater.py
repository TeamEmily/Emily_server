def create_trainingSet(words, classes, documents):
    training = []
    output = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]

        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        training.append(bag)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        output.append(output_row)