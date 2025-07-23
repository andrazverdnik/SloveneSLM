import string
from progress.bar import ShadyBar
corpusPath = "corpus.txt"
cleanCorpusPath = "cleanCorpus.txt"

corpus = open(corpusPath, "r")
lines = corpus.readlines()
newLines = []
table = str.maketrans('', '', string.digits + string.punctuation + "'…`~’‘»«–‹›‚“”")

bar = ShadyBar("Cleaning", max=len(lines))
for line in lines:
  bar.next()
  if len(line.split(" "))>3:
    newLines.append(" ".join(line.translate(table).lower().strip().split())+"\n")
bar.finish()

cleanCorpus = open(cleanCorpusPath, "w")
cleanCorpus.writelines(newLines)
cleanCorpus.close()
corpus.close()

