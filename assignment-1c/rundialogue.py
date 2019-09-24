preferences = {'food': None, 'area': None, 'pricerange': None}
state = 'welcome'


def newState(oldstate, input):
    return 'welcome'

while True:
    #give some output to the user
    print('hello!!!!')

    sentence = input()
    sentence = sentence.lower()

    #interpret input, get new state
    state = newState(state, sentence)
    
    #save relevant data
