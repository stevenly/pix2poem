
# coding: utf-8

# In[1]:

import numpy as np
from random import shuffle

from keras.preprocessing import text
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import RMSprop
from keras.utils import np_utils


# In[2]:

line_lst = []

with open('poembot/justpoems.txt') as model_file:
    for line in model_file:
        line_lst.append(line[:-1])


# In[3]:

poem_lst = []
vocabulary = set()
tmp_lst = []
start_symbol = 'q0'
end_symbol = 'qn'
unknown = 'ukn'

# Separate each poem
for line in line_lst:
    if line != '':
        line = line.lower()
        for token in line.split():
            if token[-1] == '.':
                token = token[:-1]
            vocabulary.add(token)
        tmp_lst.append(line)
    else:
        poem_lst.append(tmp_lst)
        tmp_lst = []
        
vocabulary.add(start_symbol)
vocabulary.add(end_symbol)
vocabulary.add(unknown)


# In[4]:

vocab_index = list(vocabulary)
vocab_dict = {}
for i, word in enumerate(vocabulary):
    vocab_dict[word] = i


# In[5]:

shuffle(poem_lst)


# In[6]:

# Split training, validation, and test datasets
test_size = int(len(poem_lst)*0.05)
val_size = int(len(poem_lst)*0.1)
train_size = len(poem_lst) - val_size - test_size

train_poem = poem_lst[:train_size]
val_poem = poem_lst[train_size:train_size+val_size]
test_poem = poem_lst[train_size+val_size:]

# In[7]:

max_length = 120 #Maximum word-level length of the sonnets


# In[27]:

# Constructing the model with 1 LSTM layer and 1 output layer
model = Sequential()
#model.add(Embedding(len(vocabulary), 128, embeddings_initializer='uniform'))
#model.add(Activation('relu'))
model.add(LSTM(128 , input_shape=(max_length, len(vocabulary)), activation='tanh',
               recurrent_activation='tanh', dropout=0.5, recurrent_dropout=0.5, return_sequences=True))
model.add(Dense(len(vocabulary)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='RMSprop',
	metrics=['accuracy'])


# In[ ]:

sub_poem_size = 100
poem_group_num = len(train_poem)/sub_poem_size
rem = len(train_poem)%sub_poem_size

if rem != 0:
    poem_group_num += 1
    
# Iterate through all the poem splits to handle memory issue
for i in xrange(poem_group_num):
    input_lst = []
    output_lst = []

    ptr = 0

    if i != poem_group_num-1:
        tmp_train_poem = train_poem[ptr:ptr+sub_poem_size]
    else:
        tmp_train_poem = train_poem[ptr:]

    # Create one-hot vector sequences of inputs and outputs to feed into the model
    for poem in tmp_train_poem:
        inp_tmp = []
        out_tmp = []

        #inp_tmp.append(list([vocab_dict[start_symbol]]))

        q0_tmp = np.zeros(len(vocabulary), dtype=np.float32)
        q0_tmp[vocab_dict[start_symbol]] = 1.0
        inp_tmp.append(q0_tmp)


        for line in poem:
            for token in line.split():
                if token[-1] == '.':
                    token = token[:-1]

                one_hot = np.zeros(len(vocabulary))
                one_hot[vocab_dict[token]] = 1

                #inp_tmp.append(list([vocab_dict[token]]))
                inp_tmp.append(one_hot)
                out_tmp.append(one_hot)

        #out_tmp.append(list([vocab_dict[end_symbol]]))

        end_tmp = np.zeros(len(vocabulary), dtype=np.float32)
        end_tmp[vocab_dict[end_symbol]] = 1
        out_tmp.append(end_tmp)

        # Zero padding when the poem's length is shorter 
        if len(inp_tmp) < max_length:
            diff = max_length - len(inp_tmp)

            pad_array = np.zeros([diff, len(vocabulary)])

            inp_tmp = np.vstack((pad_array, inp_tmp))
            out_tmp = np.vstack((pad_array, out_tmp))

        input_lst.append(np.array(inp_tmp))
        output_lst.append(np.array(out_tmp))

    x = np.array(input_lst)
    y = np.array(output_lst)

    model.fit(x, y, batch_size=50, nb_epoch=2, verbose=1)

    ptr += sub_poem_size


# In[19]:

# Check the error on validation data (similar to training step)
val_inp_lst = []
val_out_lst = []

for poem in val_poem:
    inp_tmp = []
    out_tmp = []

    q0_tmp = np.zeros(len(vocabulary), dtype=np.float32)
    q0_tmp[vocab_dict[start_symbol]] = 1.0
    inp_tmp.append(q0_tmp)


    for line in poem:
        for token in line.split():
            if token[-1] == '.':
                token = token[:-1]

            one_hot = np.zeros(len(vocabulary))
            one_hot[vocab_dict[token]] = 1

            #inp_tmp.append(list([vocab_dict[token]]))
            inp_tmp.append(one_hot)
            out_tmp.append(one_hot)

    #out_tmp.append(list([vocab_dict[end_symbol]]))

    end_tmp = np.zeros(len(vocabulary), dtype=np.int)
    end_tmp[vocab_dict[end_symbol]] = 1
    out_tmp.append(end_tmp)

    if len(inp_tmp) < max_length:
        diff = max_length - len(inp_tmp)

        pad_array = np.zeros([diff, len(vocabulary)])

        inp_tmp = np.vstack((pad_array, inp_tmp))
        out_tmp = np.vstack((pad_array, out_tmp))

    input_lst.append(np.array(inp_tmp))
    output_lst.append(np.array(out_tmp))

val_x = np.array(input_lst)
val_y = np.array(output_lst)

score = model.evaluate(val_x, val_y, verbose=1)
print 'Accuracy: %.2% %%' % (score[1] * 100.)

model.save('models/LSTM_word_level.h5')
