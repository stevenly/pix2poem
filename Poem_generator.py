
# coding: utf-8

# In[46]:

import numpy as np
import re
from random import shuffle


# In[2]:

line_lst = []

with open('models/metadata.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])
        
vocab_size = int(line_lst[0].split(':')[-1])
line_lst = line_lst[1:]

vocab_index = []
vocab_dict = {}

for i in xrange(vocab_size):
    wid, word = line_lst[i].split()
    vocab_index.append(word)
    vocab_dict[word] = wid

# Reading unigram file
line_lst = []

with open('models/unigram.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])
        
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

# In[53]:

gen_poem = []
start_words = np.argsort(unigrams)[-100:]
shuffle(start_words)
used_words = set()
for i in range(14):
    poem_line = [vocab_index[start_words[i]]]
    used_words.add(vocab_index[start_words[i]])
    for j in range(6):
        index = -1
        '''
        if i == j == 0 or gen_poem[-1] not in bigrams:
            indices = np.argsort(unigrams)[-40:]
            for k in range(1,41):
                if vocab_index[indices[-k]] not in used_words:
                    index = indices[-k]
                    break
        '''
        indices = np.argsort(bigrams[poem_line[-1]])[-20:]
        for k in range(1,len(indices)+1):
            if vocab_index[indices[-k]] not in used_words:
                index = indices[-k]
                break
                    
        if index == -1:
            indices = np.argsort(unigrams)[-40:]
            for k in range(1,41):
                if vocab_index[indices[-k]] not in used_words:
                    index = indices[-k]
                    break
                        
            #print index,
        
        word = vocab_index[index]
        used_words.add(word)
        poem_line.append(word)
     
    for j in xrange(len(poem_line)):
        print(poem_line[j], end='')
        
    print('')
        
    gen_poem.append(poem_line)
