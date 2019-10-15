"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1b

This file defines a rule-based tagger for dialogue acts
"""


import random

filepath = './trainData.txt'


#read training data

lines = []
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       lines.append(line.strip())
       line = fp.readline()
       cnt += 1
totalLines = cnt

#split lines in data into acts and sentences

acts = []
sentences = []

count  = 0

while(count < len(lines)):
    sentences.append(lines[count].split(" ", 1)[1])
    acts.append(lines[count].split(" ", 1)[0])
    count = count + 1

count = 0
bool = False
x = 0

#get a list of tags without duplicates

labels = []

while (count < len(acts)):
    if acts[count] not in labels:
        labels.append(acts[count])
    count = count + 1


#make an array to count how many times each tag is repeated

count = 0
count2 = 0

#frequencyArray lists the labels and their frequency
frequencyArray = [[label, 0] for label in labels]


while (count < len(acts)):
        while (count2 < len(labels)):
            if (acts[count] == labels[count2]):
                frequencyArray[count2][1] += 1
            count2 = count2 + 1
        count = count + 1
        count2 = 0

#normalise arrayOfRepetion by dividing each frequency by the total

count = 0
while (count < len(frequencyArray)):
    frequencyArray[count][1] = frequencyArray[count][1] / totalLines
    count = count + 1


#sort the array
frequencyArray = sorted(frequencyArray, key = lambda t: t[1], reverse=True)


count = 0
count2 = 0

#change frequences so they are incremental

while (count < len(frequencyArray) - 1):
    frequencyArray[count + 1][1] += frequencyArray[count][1]
    count = count + 1



count = 0
count2 = 0

# go through the training data and classify each sentence (for evaluation)

while (count < len(sentences)):
    randNumber = random.random()
    while ((frequencyArray[count2][1] < randNumber) and (count2 < len(frequencyArray) - 1)):
        count2 = count2 + 1
    sentences[count] = frequencyArray[count2][0] + ' ' +  sentences[count]
    count2 = 0
    count  = count + 1

#classify a user sentence

def userSentence(sentence):
    count2 = 0
    randNumber = random.random()
    while ((frequencyArray[count2][1] < randNumber) and (count2 < len(frequencyArray) - 1)):
        count2 = count2 + 1
    return (frequencyArray[count2][0])

#run loop to classify user input
contatore = 0 
total = 0
x = 0
while True:
    
    
    sentence = input()
    while (x < len(sentences)):
        if (lines[x] == sentences[x]):
            contatore = contatore + 1
        total = total + 1
        x = x + 1
    print (contatore)
    print (total)
    #print (sentences[1])
    if sentence == 'exit':
        ## uncomment this part to see results for all training data
        ## sentences is the combination between the prediction and the sentence as in the format it was given
        ## ( [prediction] + [sentence])

        #while (x < len(sentences)):
        #    print (sentences[x])
        #    x = x + 1
        break

    print(userSentence(sentence))
