from smartclassifier import parseExample

#pathnames
trainpath = 'trainData.txt'
testpath = 'testData.txt'

with open(trainpath, 'r') as file:
    traindata = file.readlines()

with open(testpath, 'r') as file:
    testdata = file.readlines()

data = [parseExample(instance) for instance in traindata + testdata]


lengths = sorted([len(sentence.split()) for tag, sentence in data])

mean_utterance_length = sum(lengths) / len(lengths)
median_utterance_length = lengths[int(len(lengths) / 2)]
print(median_utterance_length)

print(mean_utterance_length)
