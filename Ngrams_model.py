
# coding: utf-8

# In[1]:

import numpy as np
import re


# In[2]:

line_lst = []

with open('poembot/justpoems.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])
        
#print line_lst


# In[3]:

def abs_discount(count):
    discount_rate = (count-0.75)/count
    return discount_rate


# In[4]:

poem_lst = []
tmp_lst = []

start_symbol = 'q0'
end_symbol = 'qn'
unknown = 'ukn'

symbols = ['¿']

tri_count = {}
bi_count = {}
uni_count = {}

vocabulary = set()

total_count = 0

for line in line_lst:
    w1 = ''
    w2 = ''
    if line != '':
        
        line = line.lower()
        
        for token in line.split():
            token = re.sub('[¿.?!,;)"]', '', token)
            if len(token) == 0 or token == ' ':
                continue
                
            total_count += 1
            vocabulary.add(token)
            
            if w1 == '': 
                if token not in uni_count:
                    uni_count[token] = 1
                else:
                    uni_count[token] += 1
            elif w2 == '':
                if token not in uni_count:
                    uni_count[token] = 1
                else:
                    uni_count[token] += 1
                    
                if w1 not in bi_count:
                    bi_count[w1] = dict()
                    bi_count[w1][token] = 1
                else:
                    if token not in bi_count[w1]:
                        bi_count[w1][token] = 1
                    else:
                        bi_count[w1][token] += 1
                        
            else:
                if token not in uni_count:
                    uni_count[token] = 1
                else:
                    uni_count[token] += 1
                    
                if w1 not in bi_count:
                    bi_count[w1] = dict()
                    bi_count[w1][token] = 1
                else:
                    if token not in bi_count[w1]:
                        bi_count[w1][token] = 1
                    else:
                        bi_count[w1][token] += 1
                
                if w2 not in tri_count:
                    tri_count[w2] = dict()
                    tri_count[w2][w1] = dict()
                    tri_count[w2][w1][token] = 1
                elif w1 not in tri_count[w2]:
                    tri_count[w2][w1] = dict()
                    tri_count[w2][w1][token] = 1
                else:
                    if token not in tri_count[w2][w1]:
                        tri_count[w2][w1][token] = 1
                    else:
                        tri_count[w2][w1][token] += 1
                
            w2 = w1
            w1 = token
            
        tmp_lst.append(line)
    else:
        poem_lst.append(tmp_lst)
        tmp_lst = []
        
#vocabulary.add(start_symbol)
#vocabulary.add(end_symbol)
#vocabulary.add(unknown)


# In[5]:

vocab_index = list(vocabulary)
vocab_dict = {}
for i, word in enumerate(vocabulary):
    vocab_dict[word] = i


# In[8]:

print len(uni_count)
print len(bi_count)
print len(tri_count)


# In[8]:

bi_prob = {}
bi_leftover = {}

for w1 in bi_count:
    if w1 not in bi_prob:
        bi_prob[w1] = dict()
        bi_leftover[w1] = 1

    uni_gram_count = float(uni_count[w1])

    for w0 in bi_count[w1]:
        bi_prob[w1][w0] = (bi_count[w1][w0]/uni_gram_count)*abs_discount(bi_count[w1][w0])
        bi_leftover[w1] -= bi_prob[w1][w0]


# In[9]:

uni_prob = {}
for w0 in uni_count:
    uni_prob[w0] = uni_count[w0]/float(total_count)


# In[10]:

bi_alpha = {}
for w1 in bi_leftover:
    tmp_prob = 0
    for w0 in vocabulary:
        if w0 not in bi_count[w1]:
            tmp_prob += uni_prob[w0]
            
    bi_alpha[w1] = bi_leftover[w1]/tmp_prob


# In[11]:

bigrams = np.zeros((len(vocabulary), len(vocabulary)))

for i in xrange(len(vocabulary)):
    for j in xrange(len(vocabulary)):
        if vocab_index[i] in bi_prob and vocab_index[j] in bi_prob[vocab_index[i]]:
            bigrams[i][j] = bi_prob[vocab_index[i]][vocab_index[j]]
        elif vocab_index[i] not in bi_prob:
            bigrams[i][j] = uni_prob[vocab_index[j]]
        else:
            bigrams[i][j] = bi_alpha[vocab_index[i]]*uni_prob[vocab_index[j]]


# In[17]:

print np.sum(bigrams[0,:])


# In[18]:

tri_prob = {}
tri_leftover = {}

for w2 in tri_count:
    if w2 not in tri_prob:
        tri_prob[w2] = dict()
        #beta_dict[w2] = dict()
        tri_leftover[w2] = dict()
    for w1 in tri_count[w2]:
        if w1 not in tri_prob[w2]:
            tri_prob[w2][w1] = dict()
            #beta_dict[w2][w1] = list()
            tri_leftover[w2][w1] = 1
            
        bi_gram_count = float(bi_count[w2][w1])
        
        for w0 in tri_count[w2][w1]:
            tri_prob[w2][w1][w0] = (tri_count[w2][w1][w0]/bi_gram_count)*abs_discount(tri_count[w2][w1][w0])
            tri_leftover[w2][w1] -= tri_prob[w2][w1][w0]


# In[ ]:

tri_alpha = {}
for w2 in tri_leftover:
    tri_alpha[w2] = dict()
    for w1 in tri_leftover[w2]:
        tmp_prob = 0
        for w0 in vocabulary:
            if w0 not in tri_count[w2][w1]:
                tmp_prob += bigrams[vocab_dict[w1]][vocab_dict[w0]]

        tri_alpha[w2][w1] = tri_leftover[w2][w1]/tmp_prob


# In[ ]:

trigrams = np.zeros((len(vocabulary), len(vocabulary), len(vocabulary)))

for i in xrange(len(vocabulary)):
    for j in xrange(len(vocabulary)):
        for k in xrange(len(vocabulary)):
            if vocab_index[i] in tri_prob and vocab_index[j] in tri_prob[vocab_index[i]] and vocab_index[k] in tri_prob[vocab_index[i]][vocab_index[j]]:
                trigrams[i][j][k] = tri_prob[vocab_index[i]][vocab_index[j]][vocab_index[k]]
            elif vocab_index[i] not in tri_prob or vocab_index[j] not in tri_prob[vocab_index[i]]:
                trigrams[i][j][k] = bigrams[j][k]
            else:
                trigrams[i][j][k] = tri_alpha[vocab_index[i]][vocab_index[j]]*bigrams[j][k]

print np.sum(trigrams)

# In[ ]:

meta_file = open('metadata.txt', 'w+')

meta_file.write('vocabulary_size:{}\n'.format(len(vocabulary)))

for index in xrange(len(vocab_index)):
    meta_file.write('{wid} {word}\n'.format(wid=index, word=vocab_index[index]))
    
meta_file.close()

unigram_file = open('unigram.txt', 'w+')
    
unigram_file.write('unigrams\n')
    
for i in xrange(len(uni_prob)):
    unigram_file.write('{wid} {prob}\n'.format(wid=i, prob=uni_prob[vocab_index[i]]))
    
unigram_file.close()

bigram_file = open('bigram.txt', 'w+')

bigram_file.write('bigrams\n')

for i in xrange(bigrams.shape[0]):
    for j in xrange(bigrams.shape[1]):
        bigram_file.write('{w1} {w0} {prob}\n'.format(w1=i, w0=j, prob=bigrams[i][j]))
        
bigram_file.close()

trigram_file = open('trigram.txt', 'w+')
        
trigram_file.write('trigrams\n')

for i in xrange(trigrams.shape[0]):
    for j in xrange(trigrams.shape[1]):
        for k in xrange(trigrams.shape[2]):
            trigram_file.write('{w2} {w1} {w0} {prob}\n'.format(w2=i, w1=j, w0=k, prob=trigrams[i][j][k]))
        
trigram_file.close()

