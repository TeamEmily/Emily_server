from konlpy.tag import Twitter

class Preprocessor:
    def __init__(self, processFormat):
        self.processFormat = processFormat

    def preprocessing(self, data):
        self.setData(data)
        self.removeDuplication()

    def removeDuplication(self):
        self.processFormat.words = list(set(self.processFormat.words))
        self.processFormat.classes = list(set(self.processFormat.classes))

    def setData(self, data):
        for obj in data['training_data']:
            tokenized_sentense = self.tokenize(obj['sentence'])
            self.processFormat.words.extend(tokenized_sentense)
            self.processFormat.documents.append((tokenized_sentense, obj['class']))
            self.processFormat.classes.append(obj['class'])

    def tokenize(self, str):
        twitter = Twitter()
        posData = twitter.pos(str.strip())
        tokenized_sentense = []
        for tupple in posData:
            tokenized_sentense.append(tupple[0])
        return tokenized_sentense