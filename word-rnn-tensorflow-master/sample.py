# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

import codecs
import sys
sys.path.insert(0, '..')

import syllable_rhyme_parser as srp
#import generate_rhyme_words as grw

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
    parser.add_argument('--topic_path', type=str, default='../poem_data/rhymes.txt',
                       help='path to the file containing a list of rhyme words')

    args = parser.parse_args()
    sample(args)

def sample(args):
    
    topic_lst = []
    if os.path.exists(args.topic_path):
        with codecs.open(args.topic_path, encoding='utf-8') as topic_file:
            for topic in topic_file:
                topic_lst.append(topic[:-1])
    else:
        topic_lst.append(args.prime)
    
    
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        
        poem_file = codecs.open('sonnets.txt', 'w', 'utf-8')
        for topic in topic_lst:
            rhyme_words = topic.split()
            #rhyme_words = grw.get_rhyme_words(topic_words)
            
            for j in range(len(rhyme_words)):
                if j != 13:
                    poem_file.write('{} '.format(rhyme_words[j]))
                else:
                    poem_file.write('{}\n'.format(rhyme_words[j]))
            
            print (rhyme_words)
            
            list.reverse(rhyme_words)
        
            state = None
        
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                gen_poem = []
                for i in range(len(rhyme_words)):
                    line, state = model.sample(sess, words, vocab, state, args.n, rhyme_words[i], args.sample, args.pick, args.width)
                    gen_poem = [line] + gen_poem
            
                gen_poem = srp.add_punc_and_capital(gen_poem)
                for line in gen_poem:
                    print (line)
                    poem_file.write('{}\n'.format(line))

        poem_file.close()

if __name__ == '__main__':
    main()
