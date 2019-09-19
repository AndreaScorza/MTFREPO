from rulebasedbaseline import rulebaseline


classifier = rulebaseline

while True:
    sentence = input()
    if sentence == 'exit':
        break
    print(classifier(sentence))
