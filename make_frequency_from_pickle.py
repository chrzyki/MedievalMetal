import gzip
import pickle
from collections import Counter

# noinspection PyUnresolvedReferences
from pickle_ngrams import BandGram


def load_pickled_band_grams(band_name):
    with gzip.open('PickledGrams/' + band_name + '.gz', 'r') as f:
        return pickle.load(f)


def calculate_gram_frequency(band_gram: BandGram, album='', gram_type='char', gram_size=3, mfw=100):
    frequencies = {}

    if not album:
        if gram_type == 'char':
            for album, char_grams in band_gram.char_grams[gram_size].items():
                frequencies[album] = Counter(tuple(sorted(i)) for i in char_grams).most_common(mfw)
        elif gram_type == 'word':
            for album, word_grams in band_gram.word_grams[gram_size].items():
                frequencies[album] = Counter(tuple(sorted(i)) for i in word_grams).most_common(mfw)
        else:
            raise ValueError
    else:
        if gram_type == 'char':
            frequencies[album] =\
                Counter(tuple(sorted(i)) for i in band_gram.char_grams[gram_size][album]).most_common(mfw)
        elif gram_type == 'word':
            frequencies[album] =\
                Counter(tuple(sorted(i)) for i in band_gram.word_grams[gram_size][album]).most_common(mfw)
        else:
            raise ValueError

    return frequencies


# Sample usage:
# in_flames_grams = load_pickled_band_grams('inflames')
# calculate_gram_frequency(in_flames_grams, 'soundtracktoyourescape', gram_type='word', gram_size=2)
