#defines the function that extracts relevant information from a pair of .json files. This function is imported in chatview.py

import json

def getChat(path):
    """Parses the pair of json files in a directory (label.json and log.json) 
    and returns a list of strings that makes up the chat transcription. The 
    list starts with two strings containing meta information, and then uses 
    one string for each turn."""
    
    actList = []
    utteranceList = []

    # read user log
    with open(path + '/label.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data) # parse
    
    #extract dialog act
    for x in range(len(obj['turns'])):
        act = str(obj['turns'][x]['semantics']['cam'])
        act = act.split('(')[0]
        actList.append(act)

    for y in range(len(obj['turns'])):
        utteranceList.append(str(obj['turns'][y]['transcription']))
        
    # read system log
    # with open(path + '/log.json', 'r') as myfile2:
    #    data2=myfile2.read()
    # obj2 = json.loads(data2) #parse
    # extract transcript
    # for y in range(len(obj2['turns'])):
    #    sysList.append(str(obj2['turns'][y]['output']['transcript']))

    #combine data into chat summary
    data = []
    # data.append('session-id: ' + str(obj2['session-id']))
    # data.append(str(obj['task-information']['goal']['text']))
    for x in range(len(actList)):
        data.append((actList[x], utteranceList[x]))
    #    chat.append('system: ' +  sysList[x])
    #    chat.append('user: ' + userList[x])


    return data
