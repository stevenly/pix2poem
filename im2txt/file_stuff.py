OLD_VOCAB_FILE = "/Users/steven/projects/models/im2txt/im2txt/trained_model/word_counts.txt"
NEW_VOCAB_FILE = "/Users/steven/projects/models/im2txt/im2txt/trained_model/word_counts.txt"

with open(OLD_VOCAB_FILE) as f:
  lines = list(f.readlines())

def clean_line(line):
  tokens = line.split()
  return "%s %s" % (eval(tokens[0]), tokens[1])

newlines = [clean_line(line) for line in lines]

with open(NEW_VOCAB_FILE, "w") as f:
  for line in newlines:
    f.write(line + "\n")
