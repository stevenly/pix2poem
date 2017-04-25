import RAKE
from translate import Translator
import generate_rhyme_words as grw
import string


def extract(text):
    stoppath = 'SmartStoplist.txt'

    rake_object = RAKE.Rake(stoppath)

    keywords = rake_object.run(text)

    translator = Translator(to_lang="es")

    punc_translator = str.maketrans('', '', string.punctuation)
    translations = []
    for x in range(0, len(keywords)):
        translation = translator.translate(keywords[x][0])
        translation = translation.translate(punc_translator)
        translations.append(translation)
        print(translation)

    return translations


def get_rhyme_words_from_caption(text):
    return grw.get_rhyme_words_image(extract(text))

