import os

corpusTxtFolderPath = "ccGigafidaV1_0-text"
numTexts = 4200
out = open("corpus.txt", "w")

for n, filename in enumerate(os.listdir(corpusTxtFolderPath)):
  if n>numTexts:
    break
  if filename.endswith(".txt"):
    filePath = os.path.join(corpusTxtFolderPath, filename)
    with open(filePath, "r") as f:
      text = f.read()
      out.write(text)
    f.close()

out.close()