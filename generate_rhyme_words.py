from gensim import models

from random import shuffle
import random

import syllable_rhyme_parser
from syllable_rhyme_parser import WordStructure

model = models.KeyedVectors.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)


def get_rhyme_words(topic_words):
    a_rhymes = []
    b_rhymes = []
    c_rhymes = []
    d_rhymes = []

    rhyme_classes = dict()

    related_words = model.most_similar(positive=topic_words, topn=1000)

    filtered_set = set()
    for key, value in related_words:
        if key.lower() not in filtered_set:
            filtered_set.add(key.lower())

    for key in filtered_set:
        ws = WordStructure(key)
        if ws.rhyme in rhyme_classes:
            rhyme_classes[ws.rhyme].append(key)
        else:
            rhyme_classes[ws.rhyme] = [key]

    valid_rhyme_class_count = 0
    valid_rhyme_classes = []
    for key, value in rhyme_classes.items():
        if len(value) >= 4:
            valid_rhyme_classes.append(key)
            valid_rhyme_class_count += 1

    while valid_rhyme_class_count < 4:
        rhyme_classes = dict()
        a = random.randint(0, 7)
        related_words = model.most_similar(positive=related_words[a][0], topn=1000)
        for key, value in related_words:
            if key.lower() not in filtered_set:
                filtered_set.add(key.lower())

        for key in filtered_set:
            ws = WordStructure(key)
            if ws.rhyme in rhyme_classes:
                rhyme_classes[ws.rhyme].append(key)
            else:
                rhyme_classes[ws.rhyme] = [key]
        valid_rhyme_class_count = 0
        valid_rhyme_classes = []
        for key, value in rhyme_classes.items():
            if len(value) >= 4:
                valid_rhyme_classes.append(key)
                valid_rhyme_class_count += 1

    shuffle(valid_rhyme_classes)
    for key in valid_rhyme_classes:
        if len(a_rhymes) == 0:
            a_rhymes = rhyme_classes[key][0:4]
        elif len(b_rhymes) == 0:
            b_rhymes = rhyme_classes[key][0:4]
        elif len(c_rhymes) == 0:
            c_rhymes = rhyme_classes[key][0:3]
        elif len(d_rhymes) == 0:
            d_rhymes = rhyme_classes[key][0:3]
        else:
            break

    classes_to_return = [a_rhymes[0], b_rhymes[0], b_rhymes[1], a_rhymes[1], a_rhymes[2], b_rhymes[2],
                         b_rhymes[3], a_rhymes[3], c_rhymes[0], d_rhymes[0], c_rhymes[1], d_rhymes[1],
                         c_rhymes[2], d_rhymes[2]]

    return classes_to_return


def get_rhyme_words_with_vocab(topic_words, vocabulary):
    a_rhymes = []
    b_rhymes = []
    c_rhymes = []
    d_rhymes = []

    rhyme_classes = dict()

    related_words = model.most_similar(positive=topic_words, topn=1000)

    filtered_set = set()
    for key, value in related_words:
        if key.lower() not in filtered_set and key.lower() in vocabulary:
            filtered_set.add(key.lower())

    for key in filtered_set:
        ws = WordStructure(key)
        if ws.rhyme in rhyme_classes:
            rhyme_classes[ws.rhyme].append(key)
        else:
            rhyme_classes[ws.rhyme] = [key]

    valid_rhyme_class_count = 0
    valid_rhyme_classes = []
    for key, value in rhyme_classes.items():
        if len(value) >= 4:
            valid_rhyme_classes.append(key)
            valid_rhyme_class_count += 1

    while valid_rhyme_class_count < 4:
        rhyme_classes = dict()
        a = random.randint(0, 7)
        related_words = model.most_similar(positive=related_words[a][0], topn=1000)
        for key, value in related_words:
            if key.lower() not in filtered_set and key.lower() in vocabulary:
                filtered_set.add(key.lower())

        for key in filtered_set:
            ws = WordStructure(key)
            if ws.rhyme in rhyme_classes:
                rhyme_classes[ws.rhyme].append(key)
            else:
                rhyme_classes[ws.rhyme] = [key]
        valid_rhyme_class_count = 0
        valid_rhyme_classes = []
        for key, value in rhyme_classes.items():
            if len(value) >= 4:
                valid_rhyme_classes.append(key)
                valid_rhyme_class_count += 1

    shuffle(valid_rhyme_classes)
    for key in valid_rhyme_classes:
        if len(a_rhymes) == 0:
            a_rhymes = rhyme_classes[key][0:4]
        elif len(b_rhymes) == 0:
            b_rhymes = rhyme_classes[key][0:4]
        elif len(c_rhymes) == 0:
            c_rhymes = rhyme_classes[key][0:3]
        elif len(d_rhymes) == 0:
            d_rhymes = rhyme_classes[key][0:3]
        else:
            break

    classes_to_return = [a_rhymes[0], b_rhymes[0], b_rhymes[1], a_rhymes[1], a_rhymes[2], b_rhymes[2],
                         b_rhymes[3], a_rhymes[3], c_rhymes[0], d_rhymes[0], c_rhymes[1], d_rhymes[1],
                         c_rhymes[2], d_rhymes[2]]

    return classes_to_return


