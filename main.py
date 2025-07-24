from supabase import create_client, Client
import numpy as np

maxN = 9
url = "http://127.0.0.1:54321"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
supabase: Client = create_client(url, key)


def nextWord(text, temperature):
    text = text.lower().split(" ")
    for n in range(maxN, 0, -1):
        if len(text) >= n - 1 and n > 1:
            response = (
                supabase.table(f"{n}gram")
                .select("endWord, probability")
                .eq("startWords", " ".join(text[len(text) - n + 1 : len(text)]))
                .execute()
            )
            if len(response.data) == 0:
                continue
            probabilites = [prob["probability"] for prob in response.data]
            probabilites = applyTemperature(probabilites, temperature)
            endWords = [endW["endWord"] for endW in response.data]
            return np.random.choice(endWords, p=probabilites)
        elif len(text) >= n - 1 and n == 1:
            response = supabase.rpc("get_random_1gram").execute()
            return response.data[0]["endword"]

def applyTemperature(data, temperature):
    newData = np.array(data)
    newDataScaled = newData ** (1 / temperature)
    sumScaledData = np.sum(newDataScaled)
    return newDataScaled / sumScaledData

def completeText(text, length, temperature):
    for i in range(length):
        newWord = f" {nextWord(text, temperature)}"
        text += newWord
        print(newWord)
    return text


while True:
    temperature = float(input("Temperatura!: "))
    length = int(input("Dolžina!: "))
    text = input("Text: \n")
    completeText(text, length, temperature)
