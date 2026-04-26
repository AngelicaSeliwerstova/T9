
import pymorphy3
from sys import argv
inFile=argv[1]
outFile=argv[2]


rows = ["йцукенгшщзхъ", "фывапролджэ", "ячсмитьбю"]

graph = {ch: set() for row in rows for ch in row}

# соседи в одной строке
for row in rows:
    for i, ch in enumerate(row):
        if i > 0:
            graph[ch].add(row[i - 1])
        if i + 1 < len(row):
            graph[ch].add(row[i + 1])

# соседи между строками
for upper, lower in zip(rows, rows[1:]):
    for i, ch in enumerate(upper):
        for j in (i - 1, i):
            if 0 <= j < len(lower):
                graph[ch].add(lower[j])
                graph[lower[j]].add(ch)

graph = {k: sorted(v) for k, v in graph.items()}


morph = pymorphy3.MorphAnalyzer()

def is_russian_word(word):
    return morph.word_is_known(word)
with open(inFile, encoding='utf-8') as f:
    a=f.read().strip()
words=[]
true_words=[]
word=''
for i in a:
    if i==' ':
        if word!='':
            words.append(word)
            word=''
    else:
        word+=i
if word!='':
        words.append(word)
for w in words:
    if is_russian_word(w):
        true_words.append(w)
    else:
        found=False
        for letty in range(len(w)):
            if w[letty] in graph:
                for p in graph[w[letty]]:
                    new_word=w[:letty]+p+w[letty+1:]
                    if is_russian_word(new_word):
                        true_words.append(new_word)
                        found=True
                        break
            if found:
                break
with open(outFile,'w',encoding='utf-8') as f:
    f.write(' '.join(true_words))