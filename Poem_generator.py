# coding: utf-8
# In[46]:

import numpy as np
import re
from random import shuffle
import syllable_rhyme_parser as srp
import generate_rhyme_words as grw

# In[2]:

line_lst = []

with open('models/metadata.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])

model_file.close()

vocab_size = int(line_lst[0].split(':')[-1])
line_lst = line_lst[1:]

vocab_index = []
vocab_dict = {}

for i in range(vocab_size):
    wid, word = line_lst[i].split()
    vocab_index.append(word)
    vocab_dict[word] = int(wid)

# Reading unigram file
line_lst = []

with open('models/unigram.txt') as model_file:
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

with open('models/bigram.txt') as model_file:
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
    
    for i in range(0, 14):
        
        # add a rhyme word at the end of the line
        poem_line = [rhyme_words[i]]
        used_words.add(rhyme_words[i])
        
        for j in range(0, 7):
            # use bayes' rule to calculate the probability backward
            bayes_prob = np.zeros(vocab_size)
            
            for w1 in bigrams:
                prev_token = poem_line[0]
                if prev_token not in vocab_dict:
                    prev_token = 'ukn'
                bayes_prob[vocab_dict[w1]] = bigrams[w1][vocab_dict[prev_token]]*unigrams[vocab_dict[w1]]
            
            index = -1
            indices = np.argsort(bayes_prob)[-20:]
            for k in range(1, len(indices) + 1):
                if vocab_index[indices[-k]] not in used_words:
                    index = indices[-k]
                    break
        
            word = vocab_index[index]
            used_words.add(word)
        poem_line = [word] + poem_line
    gen_poem.append(poem_line)

for k in range(0, 14):
    
    for j in range(0, len(gen_poem[k])):
        print(gen_poem[k][j], end=' ')
        
        print('\n')

#generate_poem('gato')
