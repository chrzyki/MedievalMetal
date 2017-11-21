from nltk import ngrams
from nltk.tokenize import word_tokenize

import pickle

with open('DarkLyricsProcessed/inflames/inflames_thejesterrace.txt', 'r') as f:
    FLAMES = f.readline()

# for tri_char in ngrams([c for c in FLAMES], 3):
#     print(tri_char)

pickle.dump(list(ngrams([c for c in FLAMES], 3)), open('PickledGrams/JesterRaceChar', 'wb'))
pickle.dump(list(ngrams(word_tokenize(FLAMES), 3)), open('PickledGrams/JesterRaceWord', 'wb'))

# FLAMES_GRAMS = ngrams(flames, 3)
#
# for gram in FLAMES_GRAMS:
#     print(gram)
#
# token = word_tokenize(flames)
#
#
# for gram in ngrams(token, 3):
#     print(gram)
