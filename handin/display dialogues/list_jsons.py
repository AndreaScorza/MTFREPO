#Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
#Assignment 1a Methods in AI Research

#defines a function that searches through the database location for the location of the json files. function is imported in chatview.py

import os

def list_jsons (path):
    """Creates list of paths, given the location of the database."""
    filelist = []
    corpora = ['dstc2_traindev', 'dstc2_test']
    for corpus in corpora:
        data_path = path + '/' + corpus + '/data'
        #loop through folders
        for dir in os.listdir(data_path):
            for subdir in os.listdir(data_path + '/' + dir):
                filelist.append(data_path + '/' + dir + '/' + subdir)
        return filelist
