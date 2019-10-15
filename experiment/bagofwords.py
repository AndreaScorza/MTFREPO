import numpy as np

class bagOfWords:
    def __init__(self, word_to_index):

        self.vocabsize = len(word_to_index)
        self.wordToIndex = word_to_index

    def bagOfWords(self, sentence):
        words = list(sentence.split())
        vector = np.zeros([self.vocabsize+1])
        for word in words:
            if word in self.wordToIndex:
                index = self.wordToIndex[word]
            else:
                index = self.vocabsize
            vector[index] += 1
        return vector
