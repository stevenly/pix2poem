# coding: utf-8

import string

input = open("poem_data/nopuncReversedPoems.txt")
output = open("poem_data/reversed_no_punctuation.txt", 'w')

exclude = set(['¿', '¡', '»', '«'])

for line in input:
    output.write(''.join(ch for ch in line if ch not in exclude))

input.close()
output.close()

