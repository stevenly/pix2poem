from gensim import models
import sys
import random

import syllable_rhyme_parser
from syllable_rhyme_parser import WordStructure

model = models.KeyedVectors.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)

topic_words = sys.argv[1:]

rhyme_classes = dict()

related_words = model.most_similar(positive=topic_words, topn=500)

for key, value in related_words:
    ws = WordStructure(key)
    if ws.rhyme in rhyme_classes:
        rhyme_classes[ws.rhyme].append(ws)
    else:
        rhyme_classes[ws.rhyme] = [ws]

a_rhymes = []
b_rhymes = []
c_rhymes = []
d_rhymes = []

for key in sorted(rhyme_classes, key=lambda k: len(rhyme_classes[k]), reverse=True):
    if len(a_rhymes) == 0:
        if len(rhyme_classes[key]) >= 4:
            a_rhymes = random.sample(rhyme_classes[key], 4)
    elif len(b_rhymes) == 0:
        if len(rhyme_classes[key]) >= 4:
            b_rhymes = random.sample(rhyme_classes[key], 4)
    elif len(c_rhymes) == 0:
        if len(rhyme_classes[key]) >= 3:
            c_rhymes = random.sample(rhyme_classes[key], 3)
        else:
            break
    elif len(d_rhymes) == 0:
        if len(rhyme_classes[key]) >= 3:
            d_rhymes = random.sample(rhyme_classes[key], 3)
            break
        else:
            break


print("A")
for i in a_rhymes:
    print(i.word)
print("B")
for i in b_rhymes:
    print(i.word)
print("C")
for i in c_rhymes:
    print(i.word)
print("D")
for i in d_rhymes:
    print(i.word)
