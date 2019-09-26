"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1b

This file trains a decision tree to classify dialogue acts
"""

import numpy as np
import sklearn as sk
from sklearn import tree
import pickle

#paths
trainpath = './trainData.txt' #location of training data
exportpath = './model.sav'
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

# evaluate the model

eval_input = []
eval_desired_output = []
for line in devdata:
    tag, sentence = parseExample(line)
    inputvector = bagofwords(sentence)
    tagindex = tagToIndex(tag)
    eval_input.append(inputvector)
    eval_desired_output.append(tagindex)

#predict classification
eval_predicted_output = model.predict(eval_input)

#get accuracy
wrong = 0
for i in range(len(eval_desired_output)):
    if eval_desired_output[i] != eval_predicted_output[i]:
        wrong += 1

accuracy = ( len(eval_predicted_output) - wrong) / len(eval_predicted_output)
