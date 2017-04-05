import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# load poems and convert to lowercase
filename = 'justpoems.txt'
raw_text = open(filename).read()
raw_text = raw_text.lower()

# create map of unique characters to integers + reverse map
chars = sorted(list(set(raw_text)))
char_to_int = dict((c,i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))

#summery of text
n_chars = len(raw_text)
n_vocab = len(chars)
print("total characters: ", n_chars)
print('total vocab: ', n_vocab)

# prepare dataset of input to output pairs encoded as integers
# 100 for now, poems about 520
seq_length = 520
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("total patterns: ", n_patterns)

# reshape X to be compatible with Keras [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X/float(n_vocab)
# One Hot encode the output var
y = np_utils.to_categorical(dataY)

# define the Long Short Term Memory model
model = Sequential()
# single hidden LSTM layer with 256 memory units and dropout of 20%
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
#second layer
model.add(LSTM(256))
model.add(Dropout(0.2))

# output layer is a Dense layer with softmax activation function
model.add(Dense(y.shape[1], activation='softmax'))
# ADAM optimization for speed
model.compile(loss = 'categorical_crossentropy', optimizer='adam')


# define the checkpoint
filepath = 'weights-imporovement-{epoch:02d}-{loss:.4f}.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,save_best_only=True,mode='min')
callbacks_list = [checkpoint]

# fit the model
model.fit(X, y, nb_epoch = 50, batch_size = 64, callbacks=callbacks_list)

