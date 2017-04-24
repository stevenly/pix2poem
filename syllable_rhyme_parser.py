#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

accented_vowels = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']
strong_vowels = ['a', 'e', 'o', 'A', 'E', 'O']
weak_vowels = ['i', 'u', 'I', 'U']
vowels = strong_vowels + weak_vowels + accented_vowels


class WordStructure:
    def __init__(self, word):

        self.word = word
        self.syllables = 0
        self.stress = []
        self.rhyme = ""
        self.starts_with_vowel = False
        self.ends_with_vowel = False

        # remove all silent h's in the input_word
        parsed_word = word.replace('h', '').replace('H', '').replace('y', 'i').replace('Y', 'I')

        # check whether the word starts or ends with a vowel sound
        if parsed_word[0] in vowels:
            self.starts_with_vowel = True
        if parsed_word[-1] in vowels:
            self.ends_with_vowel = True

        index = 0
        accented_vowel_seen = False
        vowel_indexes = []

        while index < len(parsed_word):
            if parsed_word[index] in vowels:
                vowel_phrase_index = index + 1
                while vowel_phrase_index < len(parsed_word):
                    if parsed_word[vowel_phrase_index] in vowels:
                        vowel_phrase_index += 1
                    else:
                        break
                stress_added = False
                for i in range(index, vowel_phrase_index):
                    if parsed_word[i] in accented_vowels:
                        accented_vowel_seen = True
                        self.stress.append(1)
                        vowel_indexes.append(i)
                        stress_added = True
                    elif parsed_word[i] in strong_vowels:
                        self.stress.append(0)
                        vowel_indexes.append(i)
                        stress_added = True
                if not stress_added:
                    self.stress.append(0)
                    vowel_indexes.append(vowel_phrase_index - 1)
                index = vowel_phrase_index
            else:
                index += 1

        # stress assignment: if accented vowel is seen, stress has already been assigned
        # if no accented vowel has been seen yet, assign it to the last syllable if last character is
        # consonant that is not a n or s. Otherwise, assign it the second to the last syllable.

        if not accented_vowel_seen:
            if len(self.stress) == 1:
                self.stress[0] = 1
            elif len(self.stress) != 0:
                if not self.ends_with_vowel and parsed_word[-1] != 'n' and parsed_word[-1] != 's':
                    self.stress[-1] = 1
                else:
                    self.stress[-2] = 1

        # extract rhyme word
        # first, replace all accented characters
        parsed_word = parsed_word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o')\
            .replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Ó', 'O').replace('Í', 'I').replace('Ú', 'U')

        for i in range(0, len(self.stress)):
            if self.stress[i] == 1:
                self.rhyme = parsed_word[vowel_indexes[i]:]

        self.syllables = len(self.stress)


def syllable_count(text):
    words = text.split(' ')
    word_structures = [WordStructure(word) for word in words]
    count = 0
    for i in range(0, len(word_structures)):
        # for the last word, count up to it's less stressed syllable and add one
        if i == len(words) - 1:
            # check for sinelafa where there's two consecutive words: the first word ends with a vowel, second word
            # starts with a vowel. Subtract one from the word count if so
            if i != 0:
                if word_structures[i-1].ends_with_vowel and word_structures[i].starts_with_vowel:
                    count -= 1
            last_stress_index = 0
            for j in range(0, len(word_structures[i].stress)):
                if word_structures[i].stress[j] == 1:
                    last_stress_index = j
            count += last_stress_index + 2
        else:
            if i != 0:
                if word_structures[i-1].ends_with_vowel and word_structures[i].starts_with_vowel:
                    count -= 1
            count += word_structures[i].syllables

    return count


def syllable_count_list(words):
    word_structures = [WordStructure(word) for word in words]
    count = 0
    for i in range(0, len(word_structures)):
        # for the last word, count up to it's less stressed syllable and add one
        if i == len(words) - 1:
            # check for sinelafa where there's two consecutive words: the first word ends with a vowel, second word
            # starts with a vowel. Subtract one from the word count if so
            if i != 0:
                if word_structures[i-1].ends_with_vowel and word_structures[i].starts_with_vowel:
                    count -= 1
            last_stress_index = 0
            for j in range(0, len(word_structures[i].stress)):
                if word_structures[i].stress[j] == 1:
                    last_stress_index = j
            count += last_stress_index + 2
        else:
            if i != 0:
                if word_structures[i-1].ends_with_vowel and word_structures[i].starts_with_vowel:
                    count -= 1
            count += word_structures[i].syllables

    return count


def add_punc_and_capital(poem):
    line_words = []
    for line in poem:
        line_words.append(line.split())
    pattern = random.randint(0, 1)
    poem_strings = []
    if pattern == 0:
        # capitalize start of lines
        line_words[0][0] = line_words[0][0].title()
        line_words[2][0] = line_words[2][0].title()
        line_words[4][0] = line_words[4][0].title()
        line_words[5][0] = line_words[5][0].title()
        line_words[8][0] = line_words[8][0].title()
        line_words[10][0] = line_words[10][0].title()
        line_words[11][0] = line_words[10][0].title()
        for line_word in line_words:
            temp_line = line_word[0]
            for i in range(1, len(line_word)):
                temp_line = temp_line + ' ' + line_word[i]
            poem_strings.append(temp_line)
        for i in range(0, len(line_words)):
            if i == 1 or i == 3 or i == 4 or i == 7 or i == 9 or i == 10 or i == 13:
                poem_strings[i] += '.'
            else:
                poem_strings[i] += ','
    else:
        line_words[0][0] = line_words[0][0].title()
        line_words[1][0] = line_words[1][0].title()
        line_words[4][0] = line_words[4][0].title()
        line_words[6][0] = line_words[6][0].title()
        line_words[8][0] = line_words[8][0].title()
        line_words[11][0] = line_words[11][0].title()
        line_words[13][0] = line_words[13][0].title()
        for line_word in line_words:
            temp_line = line_word[0]
            for i in range(1, len(line_word)):
                temp_line = temp_line + ' ' + line_word[i]
            poem_strings.append(temp_line)
        for i in range(0, len(line_words)):
            if i == 0 or i == 3 or i == 5 or i == 7 or i == 10 or i == 12 or i == 13:
                poem_strings[i] += '.'
            else:
                poem_strings[i] += ','
    return poem_strings






