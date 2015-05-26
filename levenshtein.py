import sys, json, codecs

def levenshtein(word1, word2):
    trans = json.loads(codecs.open('transitions.json', 'r', 'utf-8').read())
    table = [[j for j in range(len(word1) + 1)]] +\
            [[i + 1] + [None] * len(word1)
             for i in range(len(word2))]
    
    for i in range(len(word2)):
        for j in range(len(word1)):
            if word1[j] == word2[i]:
                replacement = table[i][j]
            else:
                if word1[j] + '\t' + word2[i] in trans.keys():
                    replacement = table[i][j] + 1/float(trans[word1[j] + '\t' + word2[i]])
                else:
                    replacement = table[i][j] + 0.5
            insertion = table[i][j + 1] + 2
            removal = table[i + 1][j] + 1
            table[i + 1][j + 1] = min(replacement,
                                      insertion, removal)
    return table[len(word2)][len(word1)]

