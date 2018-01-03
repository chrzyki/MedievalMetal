import glob
import os

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_names = glob.glob(os.getcwd() + '/DarkLyricsProcessed/inflames/*')
vectorizer = CountVectorizer(input='filename', analyzer='word', ngram_range=(1, 6))

dtm = vectorizer.fit_transform(file_names)
dist = 1 - cosine_similarity(dtm.toarray())

names = [os.path.basename(file_name).replace('.txt', '') for file_name in file_names]

linkage_matrix = ward(dist)
dendrogram(linkage_matrix, orientation='right', labels=names)
plt.tight_layout()
plt.show()
