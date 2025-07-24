# SloveneSLM

Je eksperimentalni statistični jezikovni model, testiran na slovenščini (četudi bi moral delati tudi na drugih jezikih), temelji na N-gramih, ki se shranjujejo v supabase (ker zakaj pa ne)


## Funkcionalnosti

- Uvoz in čiščenje korpusov (Pri testiranju sem uporabljal GigafidaV1), ki so podani v obliki folderja .txt filov
- Izračun n-gramov (po defaultu od 0-9, saj moj računalnik več ni zdržal D: )
- Shranjevanje tabel n-gramov v supabase(ker ga je bilo lahko vspostaviti)
- Nastavitve temperature za model
- Fallback na manjše n-grame v primeru da večji niso najdeni
- Vstavljanje v supabase po chunkih za boljši performance

## Struktura

- compactNTexts.py združi N textov v izbranem repozitoriju v en sam txt file (corpus.txt)
- clean.py počisti corpus.txt ter ga spremeni v primeren format (cleanCorpus.txt)
- generate-n-grams uporabi cleanCorpus.txt da ven izlušči n-grame ter njihove verjetnosti ter jih pusha na supabase
- main.py uporabi to bazo za nadaljevanje texta

## Primer

```
Temperatura!: 2.5
Dolžina!: 50
Text: vsi so rekli
```

> vsi so rekli le zakaj ga pa hrčki napačne strani vožnje trčil v nasproti vozeči avtobus s katerim se je prostovoljnih gasilcev iz okolice logatca in vodic vračalo z gasilskega sejma razširil pa je tudi novoletni sejem na odru v središču mesta kulturni program pri spodnjem gradu pa pravljični luna park z velikim

