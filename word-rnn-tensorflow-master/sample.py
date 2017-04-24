from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

import sys
sys.path.insert(0, '..')

import generate_rhyme_words as grw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to load stored checkpointed models from')
    parser.add_argument('-n', type=int, default=200,
                       help='number of words to sample')
    parser.add_argument('--prime', type=str, default=' ',
                       help='prime text')
    parser.add_argument('--pick', type=int, default=1,
                       help='1 = weighted pick, 2 = beam search pick')
    parser.add_argument('--width', type=int, default=4,
                       help='width of the beam search')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        
        #['cricetomys', 'cachora', 'roedora', 'loxodontomys', 'cynomys', 'vibora', 'silbadora', 'liomys', 'barbet', 'lemur', 'civet', 'langur', 'basset', 'farfur']
        topic_words = args.prime.split()
        rhyme_words = grw.generate_rhyme_words(topic_words)
        
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            poem_gen = []
            for i in range(len(rhyme_words)):
                poem_gen.append(model.sample(sess, words, vocab, args.n, rhyme_words[i], args.sample, args.pick, args.width))

            for line in poem_gen:
                print(line)

if __name__ == '__main__':
    main()
