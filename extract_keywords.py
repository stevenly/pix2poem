import RAKE
from translate import Translator

stoppath = 'SmartStoplist.txt'

string = 'a small boat in a large body of water'

rake_object = RAKE.Rake(stoppath)

keywords = rake_object.run(string)
print ("Keywords:", keywords)

translator= Translator(to_lang="es")


for x in range(0,len(keywords)):
    translation = translator.translate(keywords[x][0])
    print('english to spanish: ', keywords[x][0],'-->', translation)

