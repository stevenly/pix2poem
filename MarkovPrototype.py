import sys
from pprint import pprint
from random import choice

EOS = ['.', '?', '!',',']


def build_dict(words):
    '''Build a Dictionary from words
    (word1, word2) -> [w1,w2,...] # key: tuple; value: list
    '''
    d = {}
    for i, word in enumerate(words):
        #tries to set all three words for trigram
        try:
            first, second, third = words[i], words[i + 1], words[i + 2]
        #breaks if end of file
        except IndexError:
            break
        #sets key as first, second tuple
        key = (first, second)
        #all keys are initialized with a empty list
        if key not in d:
            d[key] = []
        #adds third gram to key's list
        d[key].append(third)

    return d


def generate_sentence(d,begin):
    '''
    :param d: generated dictionary
    :param begin: boolean stating whether this is the beginning of the stanza or not
    :return: returns sentence/line
    '''
    #if beginning of sentence, create list of tuples with capitalized first word
    if begin:
        line = [key for key in d.keys() if key[0][0].isupper()]
    #if not begin, create list of tuples with no capitalized first word
    else:
        line = [key for key in d.keys() if key[0][0].islower()]

    #loop to ensure that [! or ? or , or .] are not present in key
    EOSdetected = True
    while EOSdetected:
        key = choice(line)
        first, second = key

        if first[-1] in EOS or second[-1] in EOS:
            EOSdetected = True
        else:
            EOSdetected = False
    line = []
    line.append(first)
    line.append(second)

    '''
        True loop to continue adding to sentence
        *If tuple has no third, end sentence creation
        *if sentence has more than 7 words, end sentence creation
    '''
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        line.append(third)
        if len(line) > 7:
            break
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(line)


#Main
#import text from file
fname = 'justpoems.txt'
with open(fname, "rt", encoding="utf-8") as f:
    text = f.read()

#splits text into words
words = text.split()

#builds dictionary from words
d = build_dict(words)
#pprint(d)


for x in range(4):
    if x == 0:
        sent = generate_sentence(d,True)
    else:
        sent = generate_sentence(d,False)
    print(sent)
print()

for x in range(4):
    if x == 0:
        sent = generate_sentence(d,True)
    else:
        sent = generate_sentence(d,False)
    print(sent)
print()
for x in range(3):
    if x == 0:
        sent = generate_sentence(d,True)
    else:
        sent = generate_sentence(d,False)
    print(sent)
print()
for x in range(3):
    if x == 0:
        sent = generate_sentence(d,True)
    else:
        sent = generate_sentence(d,False)
    print(sent)
print()

print('done')