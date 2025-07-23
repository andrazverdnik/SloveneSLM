from collections import OrderedDict, defaultdict
from progress.bar import ShadyBar
from supabase import create_client, Client

corpusPath = "cleanCorpus.txt"

url = "http://127.0.0.1:54321"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
supabase: Client = create_client(url, key)

corpus = open(corpusPath, "r")
text = corpus.readlines()
corpus.close()
mainN = 3


def getNGram(N, text):
    counter = OrderedDict()
    bar = ShadyBar(f"Going trough lines for {N}gram", max=len(text))
    for line in text:
        tokens = line.split()
        for i in range(len(tokens) - N - 1):
            Nstring = tuple(tokens[i : i + N])
            try:
                counter[Nstring] += 1
            except:
                counter[Nstring] = 1
        bar.next()
    bar.finish()
    return counter

def clearTable(N):
    while True:
        try:
            supabase.table(f"{N}gram").delete().neq("count", -1).execute()
            break
        except:
            continue

def splitCountIntoChunks(count, rowsPerChunk, N, countedStartWords):
    chunks = []
    rows = []
    i = 0
    bar = ShadyBar(f"Splitting rows into chunks for {N}gram", max=len(count))
    for key,value in count.items():
        keyStr = " ".join(key)
        startKey = key[0:N-1]
        if N == 1:
            rows.append({"string":keyStr, "startWords": " ".join(startKey), "count": value, "endWord":key[-1], "probability":float(1)})
        else:
            rows.append({"string":keyStr, "startWords": " ".join(startKey), "count": value, "endWord":key[-1], "probability":float(value/countedStartWords[startKey])})
        i += 1
        if i == rowsPerChunk:
            i = 0
            chunks.append(rows)
            rows = []
        bar.next()
    bar.finish()
    return chunks

def pushChunksIntoSupabase(N, chunks):
    bar = ShadyBar(f"Pushing into {N}gram", max=len(chunks))
    for rows in chunks:
        supabase.table(f"{N}gram").insert(rows).execute()
        bar.next()
    bar.finish()

def listStartWordsFromCount(count, N):
    if N == 1:
        return
    out = defaultdict(int)
    bar = ShadyBar(f"Counting for {N}gram", max=len(count))
    for key,value in count.items():
        start = key[0:N-1]
        out[start]+=value
        bar.next()
    bar.finish()

    return out




for i in range(mainN):
    currentN = i+1
    counter = getNGram(currentN, text)
    startWordsCounted = listStartWordsFromCount(counter, currentN)
    clearTable(currentN)
    chunks = splitCountIntoChunks(counter, rowsPerChunk=2500, N=currentN, countedStartWords=startWordsCounted)
    pushChunksIntoSupabase(currentN, chunks)


# Pol pa pojdi za vsak startWords preštet kolk jih je in iz tega za vsak entry zračunat probability. Pol pa lah nadaljevanje stavkov :)