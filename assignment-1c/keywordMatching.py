"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1c

This file matches keywords to input strings.
"""

from restaurantinfo import restaurantInfo
import Levenshtein

def findMatch(string, input):
    distancelist = []
    for word in input.split():
        distance = Levenshtein.distance(word, string)
        distancelist.append(distance)

    return min(distancelist)


def extractpreferences (input, editdistance=0):
    user_preferences = {'food': None, 'area': None, 'pricerange': None}

    #extract foor preferences
    food_distances = dict()
    for food in ['italian', 'spanish']:
        distance = findMatch(food, input)
        food_distances[food] = distance
    bestFmatch = min(food_distances, key=food_distances.get)
    if food_distances[bestFmatch] <= editdistance:
        user_preferences['food'] = bestFmatch

    #extract area preferences
    area_distances = dict()
    for area in ['north', 'east', 'south', 'west', 'centre']:
        distance = findMatch(area, input)
        area_distances[area] = distance
    bestAmatch = min(area_distances, key=area_distances.get)
    if area_distances[bestAmatch] <= editdistance:
        user_preferences['area'] = bestAmatch

    #extract price clearpreferences
    price_distances = dict()
    for price in ['cheap', 'moderately priced', 'expensive']:
        distance = findMatch(price, input)
        price_distances[price] = distance
    bestPmatch = min(price_distances, key=price_distances.get)
    if price_distances[bestPmatch] <= editdistance:
        user_preferences['pricerange'] = bestPmatch

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
