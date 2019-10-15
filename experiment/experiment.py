"""
Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)
Methods in AI Research

This file runs the experiment.
"""

# OPEN AND IMPORT

#import dialogue system
from rundialogue import dialogue

#import participant data
#filler
id = 'TEST'
condition = 1
tasks = ['You are looking for a french restaurant. Be sure to get the phone number', 'You are looking for an italian restaurant in the north side of town. If there are none, then the centre is also ok.']

# intial stuff

log = []
success_count = 0

def waitForUser():
    #wait function
    print()
    input('[press Enter to continue]')
    print()

def printOutput(output):
    print(output.upper())

# INTRODUCTION

printOutput('Hello! Thank you for participating in our experiment.')
waitForUser()

# TRIALS

for i in range(len(tasks)):
    task = tasks[i]
    last_one = i == len(tasks) - 1

    #introduce task
    printOutput('TASK:')
    printOutput(task)
    waitForUser()

    #run dialogue
    transcript, no_errors = dialogue(bool(condition))
    print()
    if no_errors:
        printOutput('You have ended the conversation.')
    else:
        printOutput('Oh no! The program encountered an unexpected error. We have to end the conversation here.')


    #ask user if they succeeded
    print()
    printOutput('Your task was:')
    printOutput(task)
    printOutput('Did you succeed in the task? [yes/no]')
    print()

    #get yes/no answer
    report = input().lower()
    print()

    valid = lambda string : string == 'yes' or string == 'no'
    while not valid(report):
        printOutput('Please answer with "yes" or "no".')
        print()
        report = input().lower()
        print()

    if report == 'yes':
        success_count += 1
        printOutput('Great!')
    else:
        printOutput('Sorry to hear it! :(')

    #update log
    log.append('\n')
    log.append('TASK: ' + task)
    log.append('SUCCEEDED: ' + report)
    log.append('ERROR RAISED: ' + str(not no_errors))
    log.append('LOG')
    log = log + transcript

    waitForUser()

# END AND REDIRECT

printOutput('Congratulations, you have completed all five tasks!')
printOutput('To continue the experiment, please fill in our questionnaire:')
print('https://forms.gle/q9km8dmXjTuLpfZYA')
printOutput('The form will ask for your pariticipant ID, so we can handle your data anonymously. Your ID is:')
print(id)
printOutput('Thank you!')

# SAVE LOG

with open('./logs/' + id + '.txt', 'w') as file:

    file.write('ID: ' + id + '\n')
    file.write('CONDITION: ' + str(condition) + '\n')
    file.write('SUCCESS COUNT: ' + str(success_count) + '\n')

    for line in log:
        file.write(line)
        file.write('\n')
