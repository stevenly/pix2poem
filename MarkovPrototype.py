import sys
from pprint import pprint
from random import choice

EOS = ['.', '?', '!',',']


def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i + 1], words[i + 2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    return d


def generate_sentence(d,begin):
    if begin:
        li = [key for key in d.keys() if key[0][0].isupper()]
    else:
        li = [key for key in d.keys() if key[0][0].islower()]

    EOSdetected = True
    while EOSdetected:
        key = choice(li)
        first, second = key

        if first[-1] in EOS or second[-1] in EOS:
            EOSdetected = True
        else:
            EOSdetected = False
    li = []
    li.append(first)
    li.append(second)
    #print(first)
    #print(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if len(li) > 7:
            break
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)

fname = 'justpoems.txt'
with open(fname, "rt", encoding="utf-8") as f:
    text = f.read()

words = text.split()
d = build_dict(words)
#pprint(d)
#print()
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