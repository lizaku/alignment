# coding: utf-8

__author__ = 'liza'

import json, codecs

cognates = []
transitions = {}
pairs = codecs.open('Levenshtein_pairs.txt', 'r', 'utf-8')
for line in pairs.readlines():
    line = line.strip()
    word, js = line.split('\t')
    word = word.split(' ')[0].lower()
    cognate = json.loads(js)[0][0].lower()
    cognates.append([word, cognate])
    for letter in range(len(word) - 1):
        try:
            if word[letter] != cognate[letter]:
                trans = (word[letter], cognate[letter])
                try:
                    transitions[trans] += 1
                except:
                    transitions[trans] = 1
        except:
            continue
js = json.dumps(transitions, ensure_ascii=False)
trns = codecs.open('transitions.json', 'w', 'utf-8')
trns.write(js)
trns.close()
final = codecs.open('transitions.csv', 'w', 'utf-8')
final.write('kazakh\ttatar\trequency\n')
for k in sorted(transitions, key=lambda k: -transitions[k]):
    final.write(k[0] + '\t' + k[1] + '\t' + str(transitions[k]) + '\n')
final.close()



