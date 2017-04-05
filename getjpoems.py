filename = 'poems.txt'
lines = []
with open(filename) as file:
    for x in file:
        lines.append(x.strip())

outputFile = open('justpoems.txt', 'w')
for x in lines:
    outputFile.write(x[18:])
    outputFile.write('\n')