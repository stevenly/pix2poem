import os



#for x in modelfile:
#    print(x)
fileToPrint=[]
root_dir = '/Users/kevinkarabinas/Desktop/NLP Project/poembot-master/Poems'
for directory, subdirectories, files in os.walk(root_dir):
    for file in files:
        if file != '.DS_Store':
            if file != 'GetPoems.py':
                if file!= 'poems.txt':
                    filename = file
                    #print(file)
                    modelfile = []
                    with open(filename) as labelfile:
                        for line in labelfile:
                            modelfile.append(line.strip())

                    for x in range(34, 54):
                        if len(modelfile[x]) > 20:
                            if x > 46:
                                fileToPrint.append(modelfile[x][10:-4] + '\n')
                            else:
                                fileToPrint.append(modelfile[x][9:-4] + '\n')
                    fileToPrint.append('\n')
#print(len(files))

outputFile = open('poems.txt', 'w')
for x in fileToPrint:
    outputFile.write(x)
    #outputFile.write('\n')
outputFile.close()

#print(len(fileToPrint))

'''


'''