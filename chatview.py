from list_jsons import list_jsons
from read_json import getChat

database_path = './dstc2_traindev'

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
for chat in chats:
    input("")
    for line in chat:
        print(line)
