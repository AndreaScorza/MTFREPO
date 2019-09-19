from list_jsons import list_jsons
from get_dialogact import getChat
import random

database_path = './data'

#export chat transcriptions

def exportchats(datapath, exportpath):
    """Export chat transcriptions to a single txt file."""
    #import data
    dirs = list_jsons(database_path)
    chats = []
    for dir in dirs:
        chat = getChat(dir)
        chats.append(chat)

    #write output file
    allActs = []
    for chat in chats:
        for line in chat:
            allActs.append(" ".join(line).lower())
    random.shuffle(allActs)

    trainingSize = int(len(allActs) * 0.85)
    trainingfile = open(exportpath + '/trainData.txt', 'w')
    for act in allActs[:trainingSize]:
        trainingfile.write(act)
        trainingfile.write('\n')
    trainingfile.close()

    testfile = open(exportpath + '/testData.txt', 'w')
    for act in allActs[trainingSize:]:
        testfile.write(act)
        testfile.write('\n')
    testfile.close()

exportchats(database_path, '.')

#return chats one by one

#read data
dirs = list_jsons(database_path)
chats = []
for dir in dirs:
    chat = getChat(dir)
    chats.append(chat)

# retrun transcripts when user presses enter
for chat in chats:
    for line in chat:
        input("")
        print(" ".join(line))
