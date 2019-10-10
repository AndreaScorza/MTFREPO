from smartclassifier import parseExample


#pathnames
trainpath = 'trainData.txt'
testpath = 'testData.txt'

with open(trainpath, 'r') as file:
    traindata = file.readlines()

with open(testpath, 'r') as file:
    testdata = file.readlines()

data = [parseExample(instance) for instance in traindata]


lengths = sorted([len(sentence.split()) for tag, sentence in data])

mean_utterance_length = sum(lengths) / len(lengths)
median_utterance_length = lengths[int(len(lengths) / 2)]

print('MLU:', mean_utterance_length)

print('length distribution:')
for i in range(max(lengths) + 1):
    print(i, sum([int(l == i) for l in lengths]) / len(lengths),  sep='\t')
print()

vocab = set(word for tag, sentence in data for word in sentence.split())

vocablist = list(word for tag, sentence in data for word in sentence.split())
freqdict = dict()
for w in vocab:
    freqdict[w] = sum([int(w == w2) for w2 in vocablist])

print('vocabulary size:', len(vocab))

uniquewords = sum([freqdict[w] == 1 for w in vocab])

print('unique words:', uniquewords)
