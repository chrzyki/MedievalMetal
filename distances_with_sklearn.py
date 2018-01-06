import glob
import os

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS

corpus = ''

# Concatenate all files and make a 'band' corpus, write this to 'band.txt':
for root, dirs, files in os.walk('experiment/'):
    _, band_name = root.split('/')

    for file in files:
        with open(os.path.join(root, file)) as out:
            corpus += out.read() + '\n'

print(corpus)

file_names = glob.glob(os.getcwd() + '/experiment/*.txt')
vectorizer = CountVectorizer(input='filename', analyzer='char', ngram_range=(4,4))

dtm = vectorizer.fit_transform(file_names)
dist = 1 - cosine_similarity(dtm.toarray())

names = [os.path.basename(file_name).replace('.txt', '') for file_name in file_names]

# Cluster

linkage_matrix = ward(dist)
dendrogram(linkage_matrix, orientation='right', labels=names)
plt.tight_layout()
plt.savefig('cluster.png')
plt.show()

# MDS Visualisation

mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
pos = mds.fit_transform(dist)

xs, ys = pos[:, 0], pos[:, 1]

for x, y, name in zip(xs, ys, names):
    color = 'orange' if "Austen" in name else 'skyblue'
    if name == 'inflames_lunarstrain':
        plt.scatter(x, y, c=color, label='lunar')
    elif name == 'inflames_thejesterrace':
        plt.scatter(x, y, c=color, label='jester race')
    else:
        plt.scatter(x, y, c=color)
    plt.text(x, y, name)

#plt.ylim(-0.5,1)
#plt.xlim(-0.5,1)
plt.legend(loc='upper left')
plt.grid()
plt.savefig('test.png', dpi=300)
plt.show()
