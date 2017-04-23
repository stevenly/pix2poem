
# coding: utf-8

# In[1]:

import numpy as np
import re
import codecs
import math

# In[2]:

line_lst = []

with codecs.open('poem_data/reversed_no_punctuation.txt', encoding='utf-8') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])
        
#print line_lst


# In[3]:

def abs_discount(count):
    discount_rate = (count-0.75)/count
    return discount_rate

def ukn_discount(count):
    discount_rate = 0.25/count
    return discount_rate


# In[4]:

poem_lst = []
tmp_lst = []

#more_to_fix = '»-:«¡'

for line in line_lst:
    if line != '':
        
        line = line.lower()
        
        token_lst = []
        
        for token in line.split():
            '''
            token = re.sub('[¿.?!,;)"]', '', token)
            if len(token) == 0 or token == ' ':
                continue
            '''
            
            token_lst.append(token)
            
        tmp_lst.append(token_lst)
    else:
        poem_lst.append(tmp_lst)
        tmp_lst = []
        
#vocabulary.add(start_symbol)
#vocabulary.add(end_symbol)
#vocabulary.add(unknown)


# In[5]:

train_size = len(poem_lst)
train_poem = poem_lst[:train_size]

# In[6]:

uni_count = {}

vocabulary = set()

total_count = 0

for poem in train_poem:
    for line in poem:
        for token in line:
            
            total_count += 1
            vocabulary.add(token)
            
            if token not in uni_count:
                uni_count[token] = 1
            else:
                uni_count[token] += 1


# # Handling rare words

# In[7]:

rare_words = set()
unknown = 'ukn'

for token in uni_count:
    if uni_count[token] == 1:
        rare_words.add(token)

uni_count[unknown] = len(rare_words)


for token in uni_count.keys():
    if token in rare_words:
        vocabulary.remove(token)
        del uni_count[token]
        
vocabulary.add(unknown)

print len(vocabulary)


# In[8]:

vocab_index = list(vocabulary)
vocab_dict = {}
for i, word in enumerate(vocabulary):
    vocab_dict[word] = i


# # Dictionary + Numpy

# In[9]:

start_symbol = 'q0'
end_symbol = 'qn'

#tri_prob = {}
bi_prob = {}

for poem in train_poem:
    w1 = ''
    #w2 = ''
    for line in poem:
        for token in line:
            
            
            # handling rare/unknown words
            if token in rare_words:
                token = unknown
            
            '''    
            if w2 != '':
                if w2 not in tri_prob:
                    tri_prob[w2] = dict()
                    
                if w1 not in tri_prob[w2]:
                    tri_prob[w2][w1] = np.zeros(len(vocabulary))
                    
                tri_prob[w2][w1][vocab_dict[token]] += 1
                    
                if w1 not in bi_prob:
                    bi_prob[w1] = np.zeros(len(vocabulary))
                    
                bi_prob[w1][vocab_dict[token]] += 1
            '''
            if w1 != '':
                if w1 not in bi_prob:
                    bi_prob[w1] = np.zeros(len(vocabulary))
                    
                bi_prob[w1][vocab_dict[token]] += 1
            
            #w2 = w1
            w1 = token


# In[10]:

line_lst = None
poem_lst = None


# In[11]:

bi_leftover = {}

for w1 in bi_prob:
    bi_leftover[w1] = 1

    uni_gram_count = float(uni_count[w1])

    for w0_id in np.where(bi_prob[w1] > 0)[0]:
        if vocab_index[w0_id] != unknown:
            bi_prob[w1][w0_id] = (bi_prob[w1][w0_id]/uni_gram_count)*abs_discount(bi_prob[w1][w0_id])
        else:
            bi_prob[w1][w0_id] = (bi_prob[w1][w0_id]/uni_gram_count)*ukn_discount(bi_prob[w1][w0_id])
            
        bi_leftover[w1] -= bi_prob[w1][w0_id]

uni_prob = np.zeros(len(vocabulary))
for i in xrange(uni_prob.shape[0]):
    uni_prob[i] = uni_count[vocab_index[i]]/float(total_count)


# In[12]:

ukn_discount = 1.0/len(rare_words)
dis_mass = uni_prob[vocab_dict[unknown]] - (uni_prob[vocab_dict[unknown]]*ukn_discount)
total_mass = np.sum(uni_prob) - uni_prob[vocab_dict[unknown]]
for i in xrange(uni_prob.shape[0]):
    if vocab_index[i] != unknown:
        uni_prob[i] += (uni_prob[i]*dis_mass)/total_mass
        
uni_prob[vocab_dict[unknown]] *= ukn_discount


# In[13]:

for w1 in bi_leftover:
    
    w0_lst = np.where(bi_prob[w1] == 0)[0]
    tmp_prob = np.sum(uni_prob[w0_lst])
    
    for w0_id in w0_lst:
        bi_prob[w1][w0_id] = (bi_leftover[w1]/tmp_prob)*uni_prob[w0_id]


# In[14]:

meta_file = codecs.open('metadata.txt', 'w', 'utf-8')

meta_file.write('vocabulary_size:{}\n'.format(len(vocabulary)))

#print  u(vocab_index[6]).encode('utf-8')

for index in xrange(len(vocabulary)):
    meta_file.write(u'{wid} {word}\n'.format(wid=index, word=vocab_index[index]))
    
meta_file.close()


# In[15]:

unigram_file = open('unigram.txt', 'w+')
    
unigram_file.write('unigrams\n')
    
for w0_id in xrange(uni_prob.shape[0]):
    unigram_file.write('{id0} {prob}\n'.format(id0=w0_id, prob=math.log(uni_prob[w0_id])))
    
unigram_file.close()


# In[16]:

bigram_file = open('bigram.txt', 'w+')

bigram_file.write('bigrams\n')

for w1 in bi_prob:
    for w0_id in xrange(bi_prob[w1].shape[0]):
        bigram_file.write('{id1} {id0} {prob},'.format(id1=vocab_dict[w1], id0=w0_id, prob=math.log(bi_prob[w1][w0_id])))
        
bigram_file.close()

