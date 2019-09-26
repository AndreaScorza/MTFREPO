

print('Loading...')

import pickle
import smartclassifier
from keywordMatching import extractpreferences
from restaurantinfo import restaurantInfo
import copy
import random

#pathnames
modelfile = 'model.sav'     #contains the trained dialogue act classifier
tagsfile = 'tags.txt'       #contains the dialogue tags (in order)
restaurantsfile = 'restaurantinfo.csv'

#parameters
alwaysAskConfirmation = False
useLevenshteinDistance = True

#import dialogue act classifier
#damodel = pickle.load(open(modelfile, 'rb'))
damodel = smartclassifier.model

#tagfile = open(tagsfile, 'r')
#text = tagfile.read()
#tags = text.split()
#tagfile.close()
tags = smartclassifier.taglist

#import restaurant data
rdata = restaurantInfo(restaurantsfile)


preferences = {'food': None, 'area': None, 'pricerange': None}
to_confirm = {'food': None, 'area': None, 'pricerange': None}
currentstate = 'welcome'
preferencestates = ['get area preference', 'get food preference', 'get pricerange preference']


def findRestaurants(preferences):
    results = []
    for res in rdata.keys():
        #check if it maches preferences
        match = True
        for field in preferences.keys():
            if preferences[field]:
                if preferences[field] != 'any' and preferences[field] != rdata[res][field]:
                    match = False

        if match:
            results.append(res)

    return results

def giveDetails(topic):
    return ''

def savePreferences(expressed, storage):
    storage = copy.deepcopy(storage)
    for field in expressed.keys():
        if expressed[field]:
            storage[field] = expressed[field]

    return storage


def generateOutput(state):
    #for states with very simple output we use a dictionary
    global preferences

    stateToOutput = { 'welcome': 'Hello! Please tell me about what kind of restaurant you would like. You can look for a price range, food type or area of town. Let\'s get cracking!',
                      'end': 'Cheerio!',
                      'start over': 'Sure, let\'s try again. What kind of food are you looking for?'}

    if state in stateToOutput:
        return stateToOutput[state]

    if state == 'ask confirmation':
        #check if the user if overriding an older choice
        for field in preferences.keys():
            oldpref = preferences[field]
            newpref = to_confirm[field]
            if oldpref and newpref and oldpref != newpref:
                return 'Do you want ' + newpref + ' instead of ' + oldpref + '?'

        #otherwise just ask for a general confirmation
        if to_confirm['pricerange']:
            pricestring = to_confirm['pricerange'] + ' '
        else:
            pricestring = ''

        if to_confirm['food']:
            foodstring = to_confirm['food'] + ' '
        else:
            foodstring = ''

        if to_confirm['area']:
            areastring = 'in the ' + to_confirm['area'] + ' part of town'
        else:
            areastring = ''

        return 'Are you looking for a fucking ' + pricestring + foodstring + 'restaurant ' + areastring + '?'


    if state in preferencestates:
        for field in preferences.keys():
            if not preferences[field]:
                confirmations = ['Sounds good!', 'Splendid!', 'Fabulous!', 'I\'m on board!', 'Perfect!', 'Lovely!', 'I\'m on it!', 'As long as I\'m invited! ']
                confirmation = random.choice(confirmations)
                return confirmation + ' What kind of ' + field + ' are you looking for?'

    if state == 'suggest':
        options = findRestaurants(preferences)
        if len(options) >= 1:
            choice = random.choice(options)
            return choice + ' might be just your thing!'
        else:
            return 'Sorry, i can\'t find anything! what about mcdonalds?'

    return 'im confused!'

def newState(oldstate, input, preferences):

    global to_confirm
    uservector = smartclassifier.bagofwords(input)
    actindex = damodel.predict([uservector])
    act = tags[actindex[0]]

    actToState = {'bye': 'end', 'thankyou': 'end', 'repeat': 'start over'}

    if act in actToState:
        return actToState[act], preferences

    if oldstate == 'welcome' or oldstate in preferencestates:
        if act == 'inform' or act == 'reqalts':
            expressedpref = extractpreferences(input)

            if oldstate in preferencestates:
                #see if the user said something like whatever/ doesnt matter, etc
                noprefstrings = ['whatever', 'any', 'doesnt matter', 'doesn\'t matter']
                nopref = False
                for string in noprefstrings:
                    if string in input:
                        nopref = True
                if nopref:
                    topic = oldstate.split()[1]
                    expressedpref[topic] = 'any'

            if useLevenshteinDistance:
                #check (maybe again) if no preferences were found: in that case use edit distance to look for typos
                anypref = False
                for field in expressedpref.keys():
                    if expressedpref[field]:
                        anypref = True

                if not anypref:
                    #use edit distance to find typos
                    expressedpref = extractpreferences(input, 2)

                    to_confirm = savePreferences(expressedpref, to_confirm)
                    return 'ask confirmation', preferences

            if alwaysAskConfirmation:
                #store preferences
                to_confirm = savePreferences(expressedpref, to_confirm)
                return 'ask confirmation', preferences
            else:
                #store preferences
                newpreferences = savePreferences(expressedpref, preferences)

                #see if a change was made
                for field in preferences.keys():
                    if preferences[field] != None:
                        if newpreferences[field] != preferences[field]:

                            to_confirm = savePreferences(newpreferences, to_confirm)
                            return 'ask confirmation', preferences

                #see if there are open fields
                for field in ['food', 'area', 'pricerange']:
                    if not newpreferences[field]:
                        return 'get ' + field + ' preference', newpreferences
                return 'suggest', newpreferences

    if act == 'affirm':
        #store preferences
        preferences = savePreferences(to_confirm, preferences)
        to_confirm = {'food': None, 'area': None, 'pricerange': None}

        #see if there are open fields
        for field in ['food', 'area', 'pricerange']:
            if not preferences[field]:
                return 'get ' + field + ' preference', preferences
        return 'suggest', preferences

    if act == 'deny':
        to_confirm = {'food': None, 'area': None, 'pricerange': None}
        for field in ['food', 'area', 'pricerange']:
            if not preferences[field]:
                return 'get ' + field + ' preference', preferences

    return 'start over', preferences

print('Done!')

while True:
    #give some output to the user
    print(generateOutput(currentstate))

    #end program if we're done
    if currentstate == 'end':
        break

    sentence = input()
    sentence = sentence.lower()

    #interpret input, get new state
    currentstate, preferences = newState(currentstate, sentence, preferences)
