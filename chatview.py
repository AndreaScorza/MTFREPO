from list_jsons import list_jsons
from read_json import getChat

database_path = '/home/luka/Documents/MAIR/ass/dstc2_traindev'

def exportchats(datapath, exportpath):
    #import data
    dirs = list_jsons(database_path)
    chats = []
    for dir in dirs[:10]:
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

exportchats(, database_path, 'chat_transcripts.txt', chats)

#return chats one by one

dirs = list_jsons(database_path)
chats = []
for dir in dirs[:10]:
    chat = getChat(dir)
    chats.append(chat)

for chat in chats:
    input("")
    for line in chat:
        print(line)
