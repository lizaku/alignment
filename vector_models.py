#!/usr/local/python/python2.7/bin/python2.7
# coding: utf-8
__author__ = 'liza'

import gensim, logging
from extract_words import extractor
import numpy as np
from sklearn import linear_model
import codecs

pairs = extractor()
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model_kz = 'kazakh_corpus.model'
# words = [line.strip().split('\t')[1].split(' ')[0] for line in codecs.open('best_neighbors.txt', 'r', 'utf-8').readlines()]
kzWords = pairs.keys()

model1 = gensim.models.Word2Vec.load(model_kz)
model1.init_sims(replace=True)

kzVectors = []
for word in kzWords:
    if word in model1:
        vector = model1[word]
        new_vector = []
        for v in vector:
            new_vector.append(float(v))
        kzVectors.append([word, new_vector])
    else:
        print word + ' is not present in the model'

model_tt = 'tatar_corpus.model'
model2 = gensim.models.Word2Vec.load(model_tt)
model2.init_sims(replace=True)

ttVectors = {}
ttWords = pairs.values()
for word in ttWords:
    if word in model2:
        vector = model2[word]
        new_vector = []
        for v in vector:
            new_vector.append(float(v))
        ttVectors[word] = new_vector
    else:
        print word + ' is not present in the model'

vectors = []
#res = codecs.open('vectors.csv', 'w', 'utf-8')
for v in kzVectors:
    try:
        vectors.append([v[1], ttVectors[pairs[v[0]]]])
    except KeyError:
        pass
#vectors[tuple(v)] = pairs[v[0]], ttVectors[pairs[v[0]]]
res = codecs.open('vector_cognates.txt', 'w', 'utf-8')

kz = np.array([x[0] for x in vectors])
tt = np.array([x[1] for x in vectors])

clf = linear_model.LinearRegression()
clf.fit(kz, tt)
kz_lemmas = codecs.open('Levenshtein_pairs.txt', 'r', 'utf-8').readlines()
for line in kz_lemmas:
    kz_lemma = line.split('\t')[0].split(' ')[0]
    try:
        vect = clf.predict([model1[kz_lemma]])
    except KeyError:
        continue
    dists = np.dot(model2.syn0norm, np.transpose(vect))
    d = [i[0] for i in dists]
    best = [[x] for x in sorted(d)[-5:]]
    sims = [np.ndarray.tolist(dists).index(b) for b in best]
    st = kz_lemma + '\t'
    for sim in sims:
        result = (model2.index2word[sim], float(dists[sim]))
        st += result[0]
        st += ' '
    res.write(st[:-1] + '\n')
res.close()