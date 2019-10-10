#defines a function that searches through the database location for the location of the json files. function is imported in chatview.py

import os

#create list of paths (given location of database)
def list_jsons (path):
    filelist = []
    corpora = ['dstc2_traindev', 'dstc2_test']
    for corpus in corpora:
        data_path = path + '/' + corpus + '/data'
        #loop through folders
        for dir in os.listdir(data_path):
            for subdir in os.listdir(data_path + '/' + dir):
                filelist.append(data_path + '/' + dir + '/' + subdir)
        return filelist
