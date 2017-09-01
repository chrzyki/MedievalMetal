import os
import re
import string
import sys

from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = SCRIPT_PATH + '/DarkLyricsProcessed/'
STOP_WORDS_FILE = open('00_Stopwords.txt', 'r')
STOP_WORDS = STOP_WORDS_FILE.read().split()


def process(file_path):
    with open(file_path, 'r') as lyrics_file:
        data = lyrics_file.read()
        soup = BeautifulSoup(data, 'html.parser')
        lyrics = soup.find('div', {'class': 'lyrics'})

        for child in lyrics.find_all('div'):
            child.decompose()

        for link in lyrics.find_all('a'):
            link.replace_with('')

        to_token = lyrics.get_text().lower().replace('\'', '').replace('-', '')
        to_token = re.sub(r'\[.*?\]', '', to_token)
        tokens = wordpunct_tokenize(to_token)

        token_string = filter(None, [
            ''.join(ch for ch in st if ch not in string.punctuation) for st in
            tokens])

        filtered = [w for w in ' '.join(token_string).split(' ') if
                    not w in STOP_WORDS]
        return ' '.join(filtered)


def main():
    for subdir, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            if f.endswith('.html'):
                lyric_path = subdir + os.sep + f
                _, band = subdir.split('/')

                if not os.path.exists(OUTPUT_PATH + band):
                    os.makedirs(OUTPUT_PATH + band)

                with open(OUTPUT_PATH + band + '/' + band + '_' + f[
                                                                  :-5] + '.txt',
                          'w+') as text_file:
                    text_file.write(process(lyric_path))


if __name__ == "__main__":
    main()
    STOP_WORDS_FILE.close()

