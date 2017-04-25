from gensim import models

from random import shuffle
import random
import numpy as np
import string

import syllable_rhyme_parser as srp
from syllable_rhyme_parser import WordStructure

model = models.KeyedVectors.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)
# model = models.KeyedVectors.load_word2vec_format('wiki.es.vec', binary=False)

line_lst = []

with open('ngram_models/metadata.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])

model_file.close()

vocab_size = int(line_lst[0].split(':')[-1])
line_lst = line_lst[1:]

beam_width = 50
vocab_index = []
vocab_dict = {}
ws_dict = {}

for i in range(vocab_size):
    wid, word = line_lst[i].split()
    vocab_index.append(word)
    vocab_dict[word] = int(wid)
    ws_dict[word] = srp.WordStructure(word)


def get_rhyme_words(topic_words):
    a_rhymes = []
    b_rhymes = []
    c_rhymes = []
    d_rhymes = []

    '''
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
    '''

    rhyme_list = get_valid_rhyme_words_size_4(topic_words, ws_dict)
    for rhyme in rhyme_list:
        if len(a_rhymes) == 0:
            a_rhymes = rhyme[0:4]
        elif len(b_rhymes) == 0:
            b_rhymes = rhyme[0:4]
        elif len(c_rhymes) == 0:
            c_rhymes = rhyme[0:3]
        elif len(d_rhymes) == 0:
            d_rhymes = rhyme[0:3]
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
        a = random.randint(0, 10)
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


def get_rhyme_words_image(image_captions):
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


def get_valid_rhyme_words_size_4(topic_words, vocabulary):

    rhyme_classes = dict()

    related_words = model.most_similar(positive=topic_words, topn=1000)

    word_prob_list = []
    filtered_set = set()

    for word in topic_words:
        filtered_set.add(word.lower())
        word_prob_list.append((word.lower(), 2))

    translator = str.maketrans('', '', string.punctuation)

    for key, value in related_words:
        word = key.lower().translate(translator)
        if word not in filtered_set:
            filtered_set.add(word)
            if word in vocabulary:
                word_prob_list.append((word, value + 1))
            else:
                word_prob_list.append((word, value))
    '''
    for i in range(0, len(top_unigram_indices)):
        if vocab_index[top_unigram_indices[i]] not in filtered_set:
            filtered_set.add(vocab_index[top_unigram_indices[i]])
            word_prob_list.append((vocab_index[top_unigram_indices[i]], 0))
    '''

    for word in word_prob_list:
        ws = WordStructure(word[0])
        if ws.rhyme in rhyme_classes:
            rhyme_classes[ws.rhyme].append(word)
        else:
            rhyme_classes[ws.rhyme] = [word]
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
            word = key.lower().translate(translator)
            if word not in filtered_set:
                filtered_set.add(word)
                if word in vocabulary:
                    word_prob_list.append((word, value + 1))
                else:
                    word_prob_list.append((word, value))

        for word in word_prob_list:
            ws = WordStructure(word[0])
            if ws.rhyme in rhyme_classes:
                rhyme_classes[ws.rhyme].append(word[0])
            else:
                rhyme_classes[ws.rhyme] = [word[0]]
        valid_rhyme_class_count = 0
        valid_rhyme_classes = []
        for key, value in rhyme_classes.items():
            if len(value) >= 4:
                valid_rhyme_classes.append(key)
                valid_rhyme_class_count += 1

    valid_rhyme_classes_prob = []
    valid_rhyme_classes_words = []
    for key in valid_rhyme_classes:
        prob_count = 0
        temp_words = []
        for word in rhyme_classes[key]:
            temp_words.append(word[0])
            prob_count = max(word[1], prob_count)
        # prob_count /= len(rhyme_classes[key])
        valid_rhyme_classes_prob.append(prob_count)
        valid_rhyme_classes_words.append(temp_words)
    return_words = []
    for i in list(reversed(np.argsort(valid_rhyme_classes_prob))):
        return_words.append(valid_rhyme_classes_words[i])
    return return_words









