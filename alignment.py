# coding: utf-8
__author__ = 'liza'

import codecs, json
from levenshtein import levenshtein

out = codecs.open(u'scores.json', u'w', u'utf-8')

kz_lexemes = {}
kz_lines = codecs.open('tt_lemmas.txt', 'r', 'utf-8').readlines()
for line in kz_lines:
    try:
        word, pos = line.strip().split('\t')[0], line.strip().split('\t')[1]
    except IndexError:
        continue
    kz_lexemes[(line.strip().split('\t')[0], line.strip().split('\t')[1])] = {}

tt_lexemes = {}
tt_lines = codecs.open('kz_lemmas.txt', 'r', 'utf-8').readlines()
for line in tt_lines:
    try:
        word, pos = line.strip().split('\t')[0], line.strip().split('\t')[1]
    except IndexError:
        continue
    tt_lexemes[(line.strip().split('\t')[0], line.strip().split('\t')[1])] = {}

for lex in kz_lexemes.keys():
    dump = {}
    for lex2 in tt_lexemes.keys():
        if lex != lex2:
            dist = levenshtein(lex[0], lex2[0])
            norm_dist = 1 - float(dist) / max(len(lex[0]), len(lex2[0]))
            if norm_dist >= 0.6:
                kz_lexemes[lex][lex2] = norm_dist
    dump['word'] = lex[0]
    dump['pos'] = lex[1]
    for key in kz_lexemes[lex]:
        dump[key[0]] = [kz_lexemes[lex][key], key[1]]
    out.write(json.dumps(dump, ensure_ascii=False) + '\n')
    #print json.dumps(dump, ensure_ascii=False)
out.close()