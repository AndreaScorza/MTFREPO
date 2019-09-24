"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1b

This file defines a rule-based tagger for dialogue acts
"""

import re

def rulebaseline (input):
    # below is a list of patterns: the first part in the tuple is a regular
    # expression that can match the target sentence, the second part is the
    # dialogue act
    rules = [ (r'thank you', 'thankyou'),
                ('bye', 'bye'),
                (r'^yes$', 'affirm'),
                (r'^wrong$', 'deny'),
                (r'^dont want', 'deny'),
                (r'^(go )?back$', 'repeat'),
                (r'^repeat', 'repeat'),
                (r'start over', 'restart'),
                (r'^im looking for', 'inform'),
                (r'^(dont care|doesnt matter)$', 'inform'),
                (r'^(okay |ok )?how about', 'reqalts'),
                (r'^next one$', 'reqalts'),
                (r'^no ', 'negate'),
                (r'(^(hi|hello))', 'hello'),
                ('else', 'reqalts'),
                (r'(address|(tele)?phone number)', 'request'),
                (r'^(kay|okay|fine)', 'ack'),
                ('could', 'request'),
                ('would like', 'inform'),
                ('more', 'reqmore'),
                ('food', 'inform'),
                ('part', 'inform'),
                ('price', 'inform'),
                ('.*', 'null')]

    #check patterns in order
    for pattern, tag in rules:
        if re.search(pattern, input):
            return tag


# testing
"""
trainfile = open('./trainData.txt', 'r')
data = trainfile.readlines()
trainfile.close()

errors = 0
total = 0
for line in data:
    words = line.split()
    true_tag = words[0]
    sentence = " ".join(words[1:])
    estimated_tag = rulebaseline(sentence)
    total += 1
    if estimated_tag != true_tag:
        errors += 1
        #print(sentence)
        #print('Real tag:', true_tag)
        #print('Estimated tag:', estimated_tag)
        #print()

print('errors:', errors)
print('error rate:', errors / total)
"""

# classify user input

while True:
    sentence = input()
    if sentence == 'exit':
        break
    print(rulebaseline(sentence))
