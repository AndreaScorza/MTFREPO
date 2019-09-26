"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1b

This file defines a rule-based tagger for dialogue acts
"""

from restaurantinfo import restaurantInfo
import Levenshtein

def findMatch(string, input, editdistance):
    if string in input:
        return True

    if editdistance > 0:
        for word in input.split():
            distance = Levenshtein.distance(word, string)
            if distance <= editdistance:
                return True

    return False


def extractpreferences (input, editdistance=0):
    user_preferences = {'food': None, 'area': None, 'pricerange': None}
    for food in foods:
        match = findMatch(food, input, editdistance)
        if match:
            user_preferences['food'] = food

    for area in areas:
        match = findMatch(area, input, editdistance)
        if match:
            user_preferences['area'] = area

    for price in priceranges:
        match = findMatch(price, input, editdistance)
        if match:
            user_preferences['pricerange'] = price

    return user_preferences

#import restaurant data
rdata = restaurantInfo('./restaurantinfo.csv')

#extract known preference options
priceranges = set()
areas = set()
foods = set()

for restaurant in rdata:
    priceranges.add(rdata[restaurant]['pricerange'])
    areas.add(rdata[restaurant]['area'])
    foods.add(rdata[restaurant]['food'])

areas.remove('') #some restaurants have blank area field

priceranges = list(priceranges)
areas = list(areas)
foods = list(foods)

# extractpreferences('i want moderately priced moroccan food in the center area of town')
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
