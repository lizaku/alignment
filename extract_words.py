# coding: utf-8

__author__ = 'liza'

import codecs, json

def extractor():
    need_lines = [4, 22, 24, 36, 37, 47, 48, 53, 6, 31, 58, 63, 66, 76, 83, 87, 91, 110, 111, 115, 134, 143, 144, 145,
                  146, 150, 153, 154, 156, 173, 211, 218, 228, 230, 233, 251, 257, 274, 288, 307, 314, 346, 352,
                  355, 356, 359, 364, 392, 393, 431, 444, 1468]
    d = codecs.open('Levenshtein_pairs.txt', 'r', 'utf-8').readlines()
    pairs = {}
    for i in need_lines:
        line = d[i - 1]
        kzWord, dump = line.split('\t')
        dump = json.loads(dump)
        ttWord = dump[0][0]
        pairs[kzWord.split('(')[0][:-1]] = ttWord

    return pairs

#extractor()