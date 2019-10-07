"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research
Assignment 1c

This file contains the main loop for the dialogue system.
"""

print('Loading...')

import smartclassifier
from keywordMatching import extractpreferences
from restaurantinfo import restaurantInfo
import copy
import random

#pathnames
modelfile = 'model.sav'     #contains the trained dialogue act classifier
tagsfile = 'tags.txt'       #contains the dialogue tags (in order)
restaurantsfile = 'restaurantinfo.csv'  #contains restaurant database

#parameters
alwaysAskConfirmation = False       #ask confirmation every time someone expresses a preference
useLevenshteinDistance = True       #use Levenshtein distance to find preferences
startSuggestingASAP = True          #suggest restaurants as soon as there is only one option left
startSuggestingImmediately = False  #suggest restaurants after the first user utterance
forceOneByeOne = False              #force user to express preferences one by one, in the order in which they are asked
maxUtterances = False               #force a maximum number of utterances by the user
textToSpeech = False                #use TTS for system utterances
<<<<<<< HEAD
=======
speechToText = False                #use STT to listen to the user
>>>>>>> master
verbose = False                     #prints extra info for debugging purposes

if textToSpeech:
    import pyttsx3
    import engineio
    
if speechToText:
    import speech_recognition as sr

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
utterancecount = 0
utterancemax = 5
testtag = None

#lookup function
def findRestaurants(preferences):
    results = []
    #loop through restaurants
    for res in rdata.keys():
        #check if it maches preferences
        match = True
        for field in preferences.keys():
            if preferences[field] and preferences[field] != 'any': #if some preference was filled in
                    if preferences[field] != rdata[res][field]: #and it doesn't match the restaurant
                        match = False

        #if there was no mismatch
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

    #for states which always need the same output, we use a dictionary
    stateToOutput = { 'welcome': 'Hello! I can help you pick a restaurant for the perfect night out. I\'d love to hear all about what kind of food you would like. Let\'s get cracking!',
                      'end': 'Cheerio!',
                      'start over': 'Sure, let\'s try again. What kind of food are you looking for?',
                      'ask to repeat': 'I\'m sorry, I don\'t know what you mean. Could you rephrase?',
                      'ran out of time': 'I don\'t think this is getting anywhere. I have places to be. Cheerio!'}

    if state in stateToOutput:
        return stateToOutput[state]

    #handling more complicated states

    #ask for confirmation
    if state == 'ask confirmation':
        #check if the user if overriding an older choice
        for field in preferences.keys():
            oldpref = preferences[field]
            newpref = to_confirm[field]
            if oldpref and newpref and oldpref != newpref:
                return 'Do you want ' + newpref + ' instead of ' + oldpref + '?'

        #otherwise just ask for a general confirmation
        #create substring for each topic
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

        #make one big statement
        return 'Are you looking for a ' + pricestring + foodstring + 'restaurant ' + areastring + '?'

    #ask for preference on a new topic
    if state in preferencestates:
        for field in preferences.keys():
            if not preferences[field]:
                confirmations = ['Sounds good!', 'Splendid!', 'Fabulous!', 'I\'m on board!', 'Perfect!', 'Lovely!', 'I\'m on it!', 'As long as I\'m invited! ']
                confirmation = random.choice(confirmations)
                return confirmation + ' What kind of ' + field + ' are you looking for?'

    #various statements in the suggesting phase
    if state == 'suggest':
        #if information was requested, provide it
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

    #classify user utterance
    uservector = smartclassifier.bagofwords(input)
    actindex = damodel.predict([uservector])
    act = tags[actindex[0]]

    #prints info for debugging purposes
    if verbose:
        print(act)

    #some acts have simple output state, which we put in a dictionary
    actToState = {'bye': 'end', 'thankyou': 'end', 'null': 'ask to repeat'}
    if act in actToState:
        return actToState[act], preferences

    #start over
    if act == 'repeat' or act == 'restart':
        #note: the user saying "start over" is classified as repeat, so we treat
        # it as a request to start over from the top, not repeat the last statement
        clearpreferences = {'food': None, 'area': None, 'pricerange': None}
        to_confirm = {'food': None, 'area': None, 'pricerange': None}
        suggestion = None
        requestedinfo = set()
        return 'start over', clearpreferences

    if oldstate == 'ask to repeat':
        #if we have a suggestion stored, continue with that
        if suggestion:
            return newState('suggest', input, preferences)

        #otherwise just ask for confirmation
        expressedpref = extractpreferences(input)
        to_confirm = savePreferences(preferences, to_confirm)
        to_confirm = savePreferences(expressedpref, to_confirm)
        return 'ask confirmation', preferences

    #interpret user preferences
    if oldstate == 'welcome' or oldstate in preferencestates or oldstate == 'start over' or oldstate == 'ask to repeat':
        if act == 'inform' or act == 'reqalts' or act == 'hello':
            #extract preferences
            expressedpref = extractpreferences(input)

            #get which topic we were asking about. Sometimes relevant.
            if oldstate in preferencestates:
                topic = oldstate.split()[1]
            else:
                topic = 'food'

            # see if the user said something like whatever/ doesnt matter, etc
            noprefstrings = ['whatever', 'any', 'doesnt matter', 'doesn\'t matter']
            nopref = False
            for string in noprefstrings:
                if string in input:
                    nopref = True
            if nopref:
                #if a no preference statement was made
                expressedpref[topic] = 'any'

            # use Levenshtein distance if applicable
            if useLevenshteinDistance:
                #check if no preferences were found: in that case use edit distance to look for typos
                anypref = any(expressedpref.values())

                if not anypref:
                    #use edit distance to find typos
                    expressedpref = extractpreferences(input, 2)    #with a bigger Levenshtein distance, chaos ensues

                    foundsomething = any(expressedpref.values())

                    if foundsomething:
                        to_confirm = savePreferences(expressedpref, to_confirm)
                        return 'ask confirmation', preferences

            #if we use the forceOneByeOne setting, the system only cares about statements on the relevant topic
            if forceOneByeOne:
                filteredpref =  {'food': None, 'area': None, 'pricerange': None}
                filteredpref[topic] = expressedpref[topic]
                expressedpref = filteredpref

            anypref = any(expressedpref.values())
            if not anypref:
                #if we still couldn´t find anything
                #if the act was hello, the user probably just said a greeting. Aks for the food type
                if act == 'hello':
                    return 'get food preference'
                #else, something went wrong. ask to repeat
                return 'ask to repeat', preferences

            #process the expressed preferences: ask for confirmation or store the directly

            if alwaysAskConfirmation:
                #store preferences
                to_confirm = savePreferences(expressedpref, to_confirm)
                return 'ask confirmation', preferences
            else:
                #store preferences
                newpreferences = savePreferences(expressedpref, preferences)

                #see if a change was made
                changed = False
                for field in preferences:
                    if preferences[field] != None:
                        if preferences[field]  != newpreferences[field]:
                            changed = True

                if changed:
                    to_confirm = savePreferences(newpreferences, to_confirm)
                    return 'ask confirmation', preferences

                #start suggesting now if startSuggestingImmediately is turned on
                if startSuggestingImmediately:
                    return 'suggest', preferences

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
            newprefs = any([expressedpref[field] for field in expressedpref])

            #if peferences were changed, move to asking for confirmation
            if newprefs:
                to_confirm = savePreferences(expressedpref, to_confirm)
                suggestion = None
                return 'ask confirmation', preferences

            #if there were preferences expressed, we assume the user wants a similar restaurant
            options = findRestaurants(preferences)
            oldsuggestion = suggestion
            options.remove(oldsuggestion)

            #if there are no alternatives left, we present the same suggestion again
            if len(options) == 0:
                return 'suggest', preferences

            suggestion = random.choice(options)
            return 'suggest', preferences

        #if the user was asking for information about the restaurant
        if act == 'request':
            requestedinfo = set()
            #keywords that match to particular topics
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

            #save which topics were mentioned
            for keyword in keywordstopics:
                if keyword in input:
                    requestedinfo.add(keywordstopics[keyword])
            return 'suggest', preferences

        if act == 'negate':
                    expressedpref = extractpreferences(input, 2)

                    to_confirm = savePreferences(expressedpref, to_confirm)
                    return 'ask confirmation', preferences

        #give more restaurants without changing anything
        if act == 'reqmore':
            options = findRestaurants(preferences)
            oldsuggestion = suggestion
            options.remove(oldsuggestion)

            if len(options) == 0:
                return 'suggest', preferences

            suggestion = random.choice(options)
            return 'suggest', preferences

    # confirmation of  the info in to_confirm
    if act == 'affirm':
        #store to_confirm to preferences and reset
        preferences = savePreferences(to_confirm, preferences)
        to_confirm = {'food': None, 'area': None, 'pricerange': None}
        suggestion = None

        #if startSuggestingImmediately
        if startSuggestingImmediately:
            return 'suggest', preferences

        #see if there is more than one restaurant left
        if startSuggestingASAP:
            options = findRestaurants(preferences)
            if len(options) == 1:
                return 'suggest', preferences

        #see if there are open fields
        for field in ['food', 'area', 'pricerange']:
            if not preferences[field]:
                return 'get ' + field + ' preference', preferences

        #if there are no opten fields, make a suggestion
        return 'suggest', preferences

    # denial of the information in to_confirm
    if act == 'deny' or 'negate':
        #reset to_confirm
        to_confirm = {'food': None, 'area': None, 'pricerange': None}

        #see if new preferences were epxressed
        expressedpref = extractpreferences(input, 2)
        anypref = any(expressedpref.values())

        if anypref:
            to_confirm = savePreferences(expressedpref, to_confirm)
            return 'ask confirmation', preferences

        #ask about new preference
        for field in ['food', 'area', 'pricerange']:
            if not preferences[field]:
                return 'get ' + field + ' preference', preferences
        #if the preference field is still full
        to_confirm = preferences
        return 'ask confirmation', preferences

    #default new state if we did not recognise the input / old state combination
    return 'ask to repeat', preferences

print('Done!\n')

while True:
    #give some output to the user
    output = generateOutput(currentstate)

    #text to speech output is available
    if textToSpeech == True:
        engineio = pyttsx3.init()
        engineio.say(output)
        engineio.runAndWait()

    #prints info for debugging purposes
    if verbose:
        print(currentstate)
        print(preferences)

    print(output)

    #presents user with info about remaining number of utterances
    if maxUtterances:
        if utterancecount != utterancemax:
            print('[', utterancemax - utterancecount, 'sentences left ]')

    #end program if we're done
    if currentstate == 'end' or currentstate == 'ran out of time':
        break

    #get user input
    if speechToText:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("I'm listening ...")                # let the user know when to speak
            audio = sr.Recognizer().listen(source)

            if verbose:
                print("sentence: " + r.recognize_google(audio))
            sentence = r.recognize_google(audio)
    else:
        sentence = input()
    
    sentence = sentence.lower()


    #interpret input, get new state
    currentstate, preferences = newState(currentstate, sentence, preferences)

    #increase utterance count
    utterancecount += 1

    #check if we exceeded maximum utterances
    if maxUtterances:
        if utterancecount >= utterancemax:
            currentstate = 'ran out of time'
