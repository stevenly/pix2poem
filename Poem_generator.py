# coding: utf-8

import numpy as np
import syllable_rhyme_parser as srp
import generate_rhyme_words as grw
import copy
import random
import gc
gc.disable()

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

# Reading unigram file
line_lst = []

with open('ngram_models/unigram.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])

model_file.close()

line_lst = line_lst[1:]
unigrams = np.zeros(vocab_size)
for line in line_lst:
    w0_id, prob = line.split()
    w0_id = int(w0_id)
    prob = float(prob)
    unigrams[w0_id] = prob

# Reading bigram file
line_lst = []

with open('ngram_models/bigram.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])

model_file.close()

line_lst = line_lst[1].split(',')
print(len(line_lst))
bigrams = {}
for line in line_lst:
    w1_id, w0_id, prob = line.split()
    w1 = vocab_index[int(w1_id)]
    w0_id = int(w0_id)
    prob = float(prob)
    if w1 not in bigrams:
        bigrams[w1] = np.zeros(vocab_size)
    bigrams[w1][w0_id] = prob


def generate_poem(topic_words):
    gen_poem = []
    used_words = set()
    # get rhyme words from text
    rhyme_words = grw.get_rhyme_words(topic_words)
    # for the 14 lines in the sonnet
    for i in range(0, 14):
        # add a rhyme word at the end of the line
        used_words.add(rhyme_words[i])
        curr_beam_search = [[rhyme_words[i]]]
        curr_beam_search_prob = [0]
        expand_beam(curr_beam_search, curr_beam_search_prob, gen_poem, used_words)
    for line in gen_poem:
        print(line)


def expand_beam(curr_beam_search, curr_beam_search_prob, gen_poem, used_words):
    for j in range(0, 16):
        # expand beams in curr_beam_search
        expanded_beam_search = []
        expanded_beam_search_prob = []
        for beam_index in range(0, len(curr_beam_search)):
            curr_sentence = curr_beam_search[beam_index]
            curr_prob = curr_beam_search_prob[beam_index]
            prev_token = curr_sentence[0]
            if prev_token not in vocab_dict:
                prev_token = 'ukn'
            # expand nodes on current beam search and add them to expanded_beam_search
            if prev_token in bigrams:
                indices = np.argsort(bigrams[prev_token])[-beam_width:]
                for k in range(0, len(indices)):
                    if vocab_index[indices[k]] not in used_words:
                        new_sentence = copy.copy(curr_sentence)
                        new_sentence.insert(0, vocab_index[indices[k]])
                        expanded_beam_search.append(new_sentence)
                        new_prob = curr_prob + bigrams[prev_token][indices[k]]
                        if vocab_index[indices[k]] in curr_sentence:
                            new_prob -= 100
                        expanded_beam_search_prob.append(new_prob)
            else:
                indices = np.argsort(unigrams)[-beam_width:]
                for k in range(0, len(indices)):
                    if vocab_index[indices[k]] not in used_words:
                        new_sentence = copy.copy(curr_sentence)
                        new_sentence.insert(0, vocab_index[indices[k]])
                        expanded_beam_search.append(new_sentence)
                        new_prob = curr_prob + unigrams[indices[k]]
                        if vocab_index[indices[k]] in curr_sentence:
                            new_prob -= 100
                        expanded_beam_search_prob.append(new_prob)
        # find the top beam-width length paths
        beam_indices_to_add = np.argsort(expanded_beam_search_prob)[-beam_width:]
        curr_beam_search = []
        curr_beam_search_prob = []
        for index in beam_indices_to_add:
            curr_beam_search.append(expanded_beam_search[index])
            curr_beam_search_prob.append(expanded_beam_search_prob[index])
        random.shuffle(curr_beam_search)
        for index in reversed(range(0, len(curr_beam_search))):
            if srp.syllable_count_list(curr_beam_search[index]) == 11:
                sentence_string = curr_beam_search[index][0]
                used_words.add(curr_beam_search[index][0])
                for a in range(1, len(curr_beam_search[index])):
                    used_words.add(curr_beam_search[index][a])
                    sentence_string = sentence_string + ' ' + curr_beam_search[index][a]
                gen_poem.append(sentence_string)
                return
            elif srp.syllable_count_list(curr_beam_search[index]) > 11:
                del curr_beam_search[index]





