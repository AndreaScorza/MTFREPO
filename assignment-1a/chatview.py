#Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
#Assignment 1a Methods in AI Research

from list_jsons import list_jsons
from read_json import getChat

database_path = '.' #remember to change this to the location of your database
                    #we assume that within the given directory, there is a directory  "data", which contains one or more directories, which contain one subdirectory for each pair of label.json and log.json files

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
    outfile = open(exportpath, 'w')
    for chat in chats:
        for line in chat:
            outfile.write(line)
            outfile.write('\n')
        outfile.write('\n\n')
    outfile.close()

exportchats(database_path, 'chat_transcripts.txt')

#return chats one by one

#read data
dirs = list_jsons(database_path)
chats = []
for dir in dirs:
    chat = getChat(dir)
    chats.append(chat)

# retrun transcripts when user presses enter
print("ready for input")
for chat in chats:
    input("")
    for line in chat:
        print(line)
