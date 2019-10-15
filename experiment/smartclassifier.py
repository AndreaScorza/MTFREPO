"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1c

This file trains a decision tree to classify dialogue acts
"""

import numpy as np
import sklearn as sk
from sklearn import tree
import pickle

#paths
trainpath = "./trainData.txt" #location of training data
exportpath = './'
tagsfile = './tags.txt'

#import training data
trainfile = open(trainpath, 'r')
data = trainfile.readlines()

#split into train and dev set with 80/20 ratio
ratio = 0.8
traindata, devdata = data[:int(len(data)*ratio)], data[int(len(data)*(1-ratio)):]
trainfile.close()

def parseExample(line):
    # split a line into a tuple with the tag and the sentence
    words = line.split()
    tag = words[0]
    sentence = " ".join(words[1:])
    return(tag, sentence)

#get a dictionary with all words in the training corpus

#we're going to sort words by their frequency, so feqdict lists the absolute frequency for each word
freqdict = dict()
tags = set()

for line in traindata:
    tag, sentence = parseExample(line)
    tags.add(tag)
    for word in sentence.split():
        if word in freqdict:
            #increase count for this word
            freqdict[word] += 1
        else:
            #otherwise, add word to dictionary with count 1
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

class bagOfWords:
    def __init__(self, vocabsize, wordToIndex):
        self.vocabsize = vocabsize
        self.wordToIndex = wordToIndex

    def bagOfWords(self, sentence):
        words = list(sentence.split())
        vector = np.zeros([vocabsize+1])
        for word in words:
            if word in wordToIndex:
                index = wordToIndex[word]
            else:
                index = vocabsize
            vector[index] += 1
        return vector


bow = bagOfWords(vocabsize, wordToIndex)

# convert tags to integers and vice versa

taglist = list(tags)

def tagToIndex(tag):
    for i in range(len(taglist)):
        if taglist[i] == tag:
            return i

def indexToTag(i):
    return taglist[i]

#get list of input and output data

train_input = list()
output = list()

for line in traindata:
    tag, sentence = parseExample(line)
    inputvector = bagofwords(sentence)
    tagindex = tagToIndex(tag)
    train_input.append(inputvector)
    output.append(tagindex)

# train a decision tree

model = sk.tree.DecisionTreeClassifier()
model.fit(train_input, output)

#export the model, tags and bagofwords function

file = open(exportpath + 'classifier.sav', 'wb')
pickle.dump(model, file)
file.close()

file = open(exportpath + 'tags.sav', 'wb')
pickle.dump(taglist, file)
file.close()

file = open(exportpath + 'bagofwords.sav', 'wb')
pickle.dump(bow, file)
file.close()
