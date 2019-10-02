Code for assignment 1c of Methods in AI research
Authors:Jos Hens (5737222), Luka van der Plas (4119142), Andrea Scorza (6649173)

###Overview of files
Our program consists of the following files:
* rundialogue.py contains the main loop for the dialogue agent: run this program to test out the agent. The code contains a state transition function and an output generating function, and imports several other modules.
* keywordMatching.py contains several functions to find preferences expressed in user utterances. It matches words in the user utterance to properties of restaurants in the database.
* restaurantinfo.py contains a function that imports the restaurant database and exports a dictionary with the information per restaurant.
* smartclassifier.py defines the dialogue act classifier, as used in assignment 1b.
* restaurantinfo.csv contains the info about restaurants, as downloaded from the main assignment.
* trainData.txt contains training data for the dialogue act classifier. We train the classifier every time (because it only takes a few seconds), so this file is essential.

###Required python packages
To run the code, the following packages should be part of your python installation:
* Levenshtein
* scikit-learn
* numpy
* pyttsx3
* speake3
* engineio

Commands to install:
```
pip install numpy
pip install scikit-learn
pip install python-Levenshtein
pip install pyttsx3
pip install speake3
pip install python-engineio
```
