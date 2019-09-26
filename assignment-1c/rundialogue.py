import pickle

#pathnames
modelfile = './model.sav'


#parameters


#import dialogue act classifier
damodel = pickle.load(open(modelfile, 'rb'))


preferences = {'food': None, 'area': None, 'pricerange': None}
to_confirm = {'food': None, 'area': None, 'pricerange': None}
state = 'welcome'



def giveDetails(topic):
    return details

def generateOutput(state):
    return 'hello!'

def newState(oldstate, input):
    return 'welcome'

while True:
    #give some output to the user
    print(generateOutput(state))

    sentence = input()
    sentence = sentence.lower()

    #interpret input, get new state
    state = newState(state, sentence)

    #save relevant data
