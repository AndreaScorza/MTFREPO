from rulebasedbaseline import rulebaseline
import smartclassifier as classifier

traindata = classifier.traindata

testfile = open('testData.txt', 'r')
testdata = testfile.readlines()
testfile.close()

#get baseline 2
#need to rewrite some stuff so it uses the same train/dev divide

import random

tags = [classifier.parseExample(instance)[0] for instance in traindata]
tagset = classifier.tags

getfreq = lambda tag : sum([int(t == tag) for t in tags])
frequencyArray = [[tag, getfreq(tag)] for tag in tagset]
frequencyArray = sorted(frequencyArray, key=lambda row: row[1], reverse=True)
total = sum([freq for tag,freq in frequencyArray])
frequencyArray = [[tag, float(freq/total)] for tag,freq in frequencyArray]
thresholdArray = [[frequencyArray[i][0], sum([frequencyArray[j][1] for j in range(i + 1)])] for i in range(len(frequencyArray))]

def stochasticbaseline(input):
    rand = random.random()
    for tag, threshold in thresholdArray:
        if rand <= threshold:
            return tag

def smartprediction(input):
    uservector = classifier.bagofwords(input)
    prediction = classifier.model.predict([uservector])
    return classifier.indexToTag(prediction[0])


sentences = [classifier.parseExample(instance)[1] for instance in testdata]
true_tags = [classifier.parseExample(instance)[0] for instance in testdata]
evaluate = lambda f : float(sum([int(f(sentences[i]) == true_tags[i]) for i in range(len(sentences))]) / len(sentences))

stochastic_acc = evaluate(stochasticbaseline
rulebased_acc = evaluate(rulebaseline)
decision_tree_acc = evaluate(smartprediction)

print('test size', len(sentences))
print('stochastic baseline', round(stochastic_acc, ndigits = 3))
print('rule-based baseline', round(rulebased_acc, ndigits = 3))
print('decision tree', round(decision_tree_acc, ndigits = 3))
