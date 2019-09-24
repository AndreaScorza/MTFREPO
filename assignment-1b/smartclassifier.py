import numpy as np
import sklearn as sk
from sklearn import tree

#paths
trainpath = './trainData.txt' #location of training data

#import training data

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
tags = set()

for line in traindata:
    tag, sentence = parseExample(line)
    tags.add(tag)
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

# get tags

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
print('training...')
model = sk.tree.DecisionTreeClassifier()
model.fit(train_input, output)

# try a sentence
#sent = 'hello'
#sentvector = bagofwords(sent)
#prediction = model.predict([sentvector])
#print(sent)
#print('prediction:', indexToTag(prediction[0]))

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

print('done!')
print('accuracy ratio:', accuracy)
print()
print('Try it yourself!')

while True:
    userinput = input()
    if userinput == 'exit':
        break

    uservector = bagofwords(userinput)
    prediction = model.predict([uservector])
    print('prediction:', indexToTag(prediction[0]))
    print()
