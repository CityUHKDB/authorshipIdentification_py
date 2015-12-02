import nltk
import re
import operator
import itertools
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

dict_of_bigrams = dict()


def count_bigrams_in_para(bigram_key):
    """This is the description"""
    if bigram_key in dict_of_bigrams:
        dict_of_bigrams[bigram_key] += 1
    else:
        dict_of_bigrams[bigram_key] = 1


def match_tokens_to_bigrams(tokens):
    """This is the description"""
    previous = ""
    tokens = [token.lower() for token in tokens]
    tagged_token = nltk.pos_tag(tokens)

    for key in tokens:
        if re.match(r'.*\w', key):
            #print "Match word: ", key
            #print "Part-of-Speech: ", val
            if not previous:
                previous = key
                continue

            count_bigrams_in_para(previous + "-" + key)
            previous = key
        #else:
        # To be added to deal with punctuation


def read_paragraphs_and_split(paragraphs):
    dict_of_bigrams = dict()
    for para in paragraphs:
        for sentence in para:
            match_tokens_to_bigrams(sentence)

#paragraphs = nltk.corpus.gutenberg.paras("shakespeare-caesar.txt")
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha1.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
key_list1 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
key_list2 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
key_list3 = itertools.islice(sorted(dict_of_bigrams.items(), key=operator.itemgetter(1), reverse=True), 0, 40)
ch1_bigram_list = [dict_of_bigrams.get(x[0]) for x in key_list1]

corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha2.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
ch2_bigram_list = [dict_of_bigrams.get(y[0]) for y in key_list2]

corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./data", "cha3.txt")
p = corpus.paras()
read_paragraphs_and_split(p)
ch3_bigram_list = [dict_of_bigrams.get(z[0]) for z in key_list3]

lists = list()
lists.append(ch1_bigram_list)
lists.append(ch2_bigram_list)
lists.append(ch3_bigram_list)

X = np.array(lists)
pca = PCA(n_components=40)
transformed_data = pca.fit(X)
pca_score = pca.explained_variance_ratio_
first_pc = pca.components_[0]
second_pc = pca.components_[1]

for i in transformed_data:
    plt.scatter( first_pc[0] * i[0], first_pc[0] * i[0], color="r")
    plt.scatter( second_pc[0] * i[0], second_pc[0] * i[0], color="c")

plt.xlabel("First Principal Component")
plt.ylabel("Second Principal Component")
plt.show()