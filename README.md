# poembot
From Picture to Poem: Spanish Sonnet Generation from Image Inputs using RNNs

New Chanuwas, Kevin Karabinas, Khanh Le, Steven Ly

Our project will use machine-created image captions to generate spanish sonnets using a bigram model as baseline, and a RNN LSTM model. 
Users can provide input text as a topic for the generated poems in the normal poetry generation mode.
Images can also be provided as input, where our system will automatically generate a caption and a poem from the caption.
We use word2vec word embeddings trained on the Spanish Billion Words corpus to get related words that are later chunked into rhyme classes. 
Our poems will be evaluated by human evaluators
on rhyme structure, fluency, and poeticness.

Word2Vec, RNN, n-gram, and image captioning models are not uploaded to Github, since their file sizes are too big.