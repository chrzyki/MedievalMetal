from nltk import ngrams
from nltk.tokenize import word_tokenize
import os

import pickle
import gzip


class BandGram:
    def make_char_grams(self):
        aggregated_char_grams = {}

        for ngram_size in range(1, self.gram_size + 1):
            album_char_grams = {}

            for album, lyrics in self.band_lyrics.items():
                album_char_grams[album] = list(ngrams([c for c in lyrics], ngram_size))
                aggregated_char_grams[ngram_size] = album_char_grams

        return aggregated_char_grams

    def make_word_grams(self):
        aggregated_word_grams = {}

        for ngram_size in range(1, self.gram_size + 1):
            album_word_grams = {}

            for album, lyrics in self.band_lyrics.items():
                album_word_grams[album] = list(ngrams(word_tokenize(lyrics), ngram_size))
                aggregated_word_grams[ngram_size] = album_word_grams

        return aggregated_word_grams

    def __init__(self, band_name: str, album_dict, char_grams: bool=True,
                 word_grams: bool=True, gram_size: int=3):
        self.band_name = band_name
        self.band_lyrics = album_dict
        self.gram_size = gram_size

        if char_grams:
            self.char_grams = self.make_char_grams()

        if word_grams:
            self.word_grams = self.make_word_grams()


def create_band_grams():
    i = 0

    for subdir, dirs, files in os.walk('DarkLyricsProcessed/'):
        _, band_name = subdir.split('/')

        if not band_name:
            continue

        band_lyrics = {}

        for f in files:
            lyric_path = subdir + os.sep + f
            album_title = lyric_path.split('_')[1].split('.')[0]

            with open(lyric_path, 'r') as lyrics_file:
                band_lyrics[album_title] = lyrics_file.readline()

        i += 1
        pickle.dump(BandGram(band_name, band_lyrics, gram_size=10),
                    gzip.open('PickledGrams/' + band_name + '.gz', 'wb'))
        print(str(i) + ": " + band_name)

if __name__ == "__main__":
    create_band_grams()
