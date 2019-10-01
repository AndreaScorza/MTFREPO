

print('Loading...')

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
alwaysAskConfirmation = False   #ask confirmation every time someone expresses a preference
useLevenshteinDistance = True   #use Levenshtein distance to find preferences
startSuggestingASAP = True      #suggest restaurants as soon as there is only one option left
forceOneByeOne = True           #force user to express preferences one by one, in the order in which they are asked

#import dialogue act classifier
damodel = smartclassifier.model
tags = smartclassifier.taglist

#import restaurant data
rdata = restaurantInfo(restaurantsfile)

#global parameters
preferences = {'food': None, 'area': None, 'pricerange': None}
to_confirm = {'food': None, 'area': None, 'pricerange': None}
suggestion = None
requestedinfo = set()
currentstate = 'welcome'
preferencestates = ['get area preference', 'get food preference', 'get pricerange preference']

#lookup function
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

#give details for a restaurant
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
    global suggestion
    global requestedinfo

    stateToOutput = { 'welcome': 'Hello! I can help you pick a restaurant for the perfect night out. I\'d love to hear all about what kind of food you would like. Let\'s get cracking!',
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

        return 'Are you looking for a ' + pricestring + foodstring + 'restaurant ' + areastring + '?'

    #Ask for a new topic
    if state in preferencestates:
        for field in preferences.keys():
            if not preferences[field]:
                confirmations = ['Sounds good!', 'Splendid!', 'Fabulous!', 'I\'m on board!', 'Perfect!', 'Lovely!', 'I\'m on it!', 'As long as I\'m invited! ']
                confirmation = random.choice(confirmations)
                return confirmation + ' What kind of ' + field + ' are you looking for?'

    if state == 'suggest':
        if len(requestedinfo) > 0:
            infostatements = []
            for topic in requestedinfo:
                #sentence templates for every topic
                topicToSentences = {'addr': ('You can find the restaurant at ', '.'),
                                    'phone': ('The phone number is ', '.'),
                                    'postcode': ('The postcode is', '.'),
                                    'pricerange': ('It\'s a fairly ', ' restaurant.'),
                                    'area': ('The restaurant is in the lovely ', ' part of town.'),
                                    'food': ('The restaurant serves ', ' food.')}
                #put the sentence halves together
                statement = topicToSentences[topic][0] + rdata[suggestion][topic] + topicToSentences[topic][1]
                infostatements.append(statement)
            requestedinfo = set()
            return ' '.join(infostatements)

        #if a suggestion is already stored in the system, just repeat it
        #this will mostly happen if the system can't make sense of the user input
        if suggestion:
            return suggestion + ' might be just your thing!'

        #if no suggestion is in the system, make a new one
        else:
            options = findRestaurants(preferences)
            if len(options) >= 1:
                choice = random.choice(options)
                suggestion = choice
                return choice + ' might be just your thing! It is a ' + rdata[choice]['pricerange'] + ' ' + rdata[choice]['food'] + ' restaurant in the ' + rdata[choice]['area'] + ' part of town.'
            else:
                return 'Sorry, i can\'t find anything like that.'

    return 'I didn\'t quite get that. Could you rephrase?'

def newState(oldstate, input, preferences):

    global to_confirm
    global suggestion
    global requestedinfo

    uservector = smartclassifier.bagofwords(input)
    actindex = damodel.predict([uservector])
    act = tags[actindex[0]]

    actToState = {'bye': 'end', 'thankyou': 'end'}

    if act in actToState:
        return actToState[act], preferences

    if act == 'repeat':
        clearpreferences = {'food': None, 'area': None, 'pricerange': None}
        return 'start over', clearpreferences

    if oldstate == 'welcome' or oldstate in preferencestates or oldstate == 'start over':
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

                #see if there is more than one restaurant left
                if startSuggestingASAP:
                    options = findRestaurants(preferences)
                    if len(options) == 1:
                        return 'suggest', preferences

                #see if there are open fields
                for field in ['food', 'area', 'pricerange']:
                    if not newpreferences[field]:
                        return 'get ' + field + ' preference', newpreferences
                return 'suggest', newpreferences

    #moving on from making a suggestion
    if oldstate == 'suggest':
        if act == 'reqalts':
            #request alternatives can mean changing preferences or asking for other options with the current preferences

            #check if the user voiced new preferences
            expressedpref = extractpreferences(input)
            newprefs = False
            for field in expressedpref:
                if expressedpref[field]:
                    newprefs = True

            #if peferences were changed
            to_confirm = savePreferences(expressedpref, to_confirm)
            return 'ask confirmation', preferences

            #if there were preferences expressed, we assume the user wants a similar restaurant
            options = findRestaurants(preferences)
            oldsuggestion = suggestion
            options.remove(oldsuggestion)
            suggestion = random.choice(options)
            return 'suggest', preferences

        if act == 'request':
            requestedinfo = set()
            keywordstopics = {'phone': 'phone',
                              'address': 'addr',
                              'where': 'addr',
                              'post': 'postcode',
                              'price': 'pricerange',
                              'how much': 'pricerange',
                              'cost': 'pricerange',
                              'type': 'food',
                              'kind': 'food',
                              'food': 'food',
                              'area': 'area'}

            for keyword in keywordstopics:
                if keyword in input:
                    requestedinfo.add(keywordstopics[keyword])
            return 'suggest', preferences

        if act == 'reqmore':
            options = findRestaurants(preferences)
            oldsuggestion = suggestion
            options.remove(oldsuggestion)
            suggestion = random.choice(options)
            return 'suggest', preferences


    if act == 'affirm':
        #store preferences
        preferences = savePreferences(to_confirm, preferences)
        to_confirm = {'food': None, 'area': None, 'pricerange': None}

        #see if there is more than one restaurant left
        if startSuggestingASAP:
            options = findRestaurants(preferences)
            if len(options) == 1:
                return 'suggest', preferences

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

    #default new state if we did not recognise the input / old state combination
    return oldstate, preferences

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
