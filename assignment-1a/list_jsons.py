#Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
#Assignment 1a Methods in AI Research

#defines a function that searches through the database location for the location of the json files. function is imported in chatview.py

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
