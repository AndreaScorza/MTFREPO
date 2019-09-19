#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:27:48 2019

@author: andrea
"""


import random
lines = []

filepath = '/Users/andrea/Desktop/cartelladilavoromethods/trainData.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       lines.append(line.strip())
       line = fp.readline()
       cnt += 1
totalLines = cnt


   
count  = 0

while(count < len(lines)):
    lines[count] = lines[count].split(" ", 1)[0]
    count = count + 1


count = 0
count2 = 0
bool = False
x = 0
labels = []

while (count < len(lines)):
    if lines[count] not in labels:
        labels.append(lines[count])
    count = count + 1




count = 0
count2 = 0
arrayOfRepetition = [0] * len(labels)

while (count < len(lines)):
        while (count2 < len(labels)):
            if (lines[count] == labels[count2]):
                arrayOfRepetition[count2] = arrayOfRepetition[count2] + 1
            count2 = count2 + 1
        count = count + 1
        count2 = 0


count = 0
while (count < len(arrayOfRepetition)):
    arrayOfRepetition[count] = arrayOfRepetition[count] / totalLines
    count = count + 1


count = 0
count2 = 0


while (count < len(arrayOfRepetition) - 1):
    arrayOfRepetition[count + 1] = arrayOfRepetition[count] + arrayOfRepetition[count + 1]
    count = count + 1


count = 0
count2 = 0
    

          

print(lines)
while (count < len(lines)):
    randNumber = random.random()
    #print(randNumber)
    while ((arrayOfRepetition[count2] < randNumber) and (count2 < 14)):
        count2 = count2 + 1
    lines[count] = lines[count] + labels[count2]
    count2 = 0
    count  = count + 1


print(lines)


