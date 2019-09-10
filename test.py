#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:27:48 2019

@author: andrea
"""



import json

def getChat(path):
    
    userList = []
    sysList = []
    
    # read file
    with open(path + '/label.josn', 'r') as myfile:
        data=myfile.read()
    
    
    # parse file
    obj = json.loads(data)
    
    
    
    
    
    for x in range(len(obj['turns'])):
        userList.append(str(obj['turns'][x]['transcription']))
        
        
    
    
    
    with open(path + '/log.josn', 'r') as myfile2:
        data2=myfile2.read()
        
    obj2 = json.loads(data2)
    
    
    for y in range(len(obj2['turns'])):
        sysList.append(str(obj2['turns'][y]['output']['transcript']))
    
    
    chat = []
    chat.append('session-id: ' + str(obj2['session-id']))
    chat.append(str(obj['task-information']['goal']['text']))
    for x in range(len(sysList)):
        chat.append('system: ' +  sysList[x])
        chat.append('user: ' + userList[x])
        
    
    return chat