#paths
trainpath = './trainData.txt' #location of training data
import numpy as np

trainfile = open(trainpath, 'r')
data = trainfile.readlines()
ratio = 0.8
traindata, devdata = data[:int(len(data)*ratio)], data[int(len(data)*(1-ratio)):]
trainfile.close()

def parseExample(line):
    words = line.split()
    tag = words[0]
    sentence = " ".join(words[1:])
    return(tag, sentence)

#get a dictionary with all words in the training corpus

freqdict = dict()

for line in traindata:
    tag, sentence = parseExample(line)
    for word in sentence.split():
        if word in freqdict:
            freqdict[word] += 1
        else:
            freqdict[word] = 1

vocab = []

for word in freqdict.keys():
    vocab.append((word))
vocab = sorted(vocab, key=lambda x: freqdict[x])

wordToIndex = dict()
for x in range(len(vocab)):
    wordToIndex[vocab[x]] = x

vocabsize = len(vocab)

def bagofwords(sentence):
    #get the input sentence as a string and return set of all the words
    words = list(sentence.split())
    vector = np.zeros([vocabsize+1])
    for word in words:
        if word in wordToIndex:
            index = wordToIndex[word]
        else:
            index = vocabsize
        vector[index] += 1
    return vector

print(bagofwords('i would like a chinese restaurant jkdfkghej'))
