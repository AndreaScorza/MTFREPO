import os

#create list of paths (given location of database)
def list_jsons (path):
    data_path = path + '/data'
    filelist = []
    #loop through folders
    for dir in os.listdir(data_path):
        for subdir in os.listdir(data_path + '/' + dir):
            filelist.append(data_path + '/' + dir + '/' + subdir)
    return filelist