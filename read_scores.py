# coding: utf-8

__author__ = 'liza'

import codecs, json
kzWords = {}
distances = {}
res = codecs.open('Levenshtein_pairs.txt', 'w', 'utf-8')
for line in codecs.open('scores.json', 'r', 'utf-8').readlines():
    js = json.loads(line)
    pos = js['pos']
    if pos == 'A':
        pos = 'ADJ'
    kzWord = js['word'] + u' (' + pos + u')'
    kzWords[kzWord] = []
    distances[kzWord] = 0.0
    for k, v in js.iteritems():
        if k in ['word', 'pos']:
            continue
        if v[1] == pos:
            kzWords[kzWord].append([k] + v)
            if v[0] > distances[kzWord]:
                distances[kzWord] = v[0]
    kzWords[kzWord].sort(key=lambda w: -w[1])
    kzWords[kzWord] = kzWords[kzWord][:3]
for word in sorted(distances, key=lambda w: -distances[w]):
    if distances[word] < 0.4:
        continue
    res.write(word + '\t' + json.dumps(kzWords[word], ensure_ascii=False) + '\n')
res.close()


