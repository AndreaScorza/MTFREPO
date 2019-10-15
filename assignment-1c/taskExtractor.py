#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:19:58 2019

@author: andrea
"""
task = []
import random

f = open("chatTranscripts.txt", "r")
for x in f:
    if "Task" in x:
        task.append(x)


j = 0
taskSelected = []

text_file = open("Output.txt", "w")

while (j < 50):
    z = random.choice(task)
    if (z not in taskSelected):
        taskSelected.append(z)
        text_file.write(z)
        j = j + 1
    
f.close()

text_file.close()

#print(taskSelected)