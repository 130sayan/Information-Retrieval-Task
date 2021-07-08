import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.metrics import f1_score
from bs4 import BeautifulSoup
from dateutil.parser import parse
import json
import datetime
import string
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import numpy as np
import sys
from collections import Counter
from math import log10
from numpy import linalg as LA
import itertools
from sklearn import pipeline, ensemble, preprocessing, feature_extraction
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.feature_extraction.text import CountVectorizer

address = os.getcwd()
newaddress = address + "/dataset/class1"
os.chdir(newaddress)
test1 = []
train1 = []
lemma = WordNetLemmatizer()

newaddress1 = newaddress+"/test"
os.chdir(newaddress1)
test1list = os.listdir(os.getcwd())
for document in test1list:

        curr_file = open(document, 'r+', errors='ignore')
        newstring = curr_file.read().replace("\n", " ")
        test1.append(newstring)

os.chdir(newaddress)
newaddress2 = newaddress+"/train"
os.chdir(newaddress2)
train1list = os.listdir(os.getcwd())
for document in train1list:

        curr_file = open(document, 'r+', errors='ignore')
        newstring = curr_file.read().replace("\n", " ")
        train1.append(newstring)

newaddress = address + "/dataset/class2"
os.chdir(newaddress)
test2 = []
train2 = []

newaddress1 = newaddress+"/test"
os.chdir(newaddress1)
test2list = os.listdir(os.getcwd())
for document in test2list:

        curr_file = open(document, 'r+', errors='ignore')
        newstring = curr_file.read().replace("\n", " ")
        test2.append(newstring)

os.chdir(newaddress)
newaddress2 = newaddress+"/train"
os.chdir(newaddress2)
train2list = os.listdir(os.getcwd())
for document in train2list:

        curr_file = open(document, 'r+', errors='ignore')
        newstring = curr_file.read().replace("\n", " ")
        train2.append(newstring)

total1 = train1+train2
total2 = test1+test2

os.chdir(address)
ar1 = np.concatenate((np.zeros(len(train1)),np.ones(len(train2))))

ar2 = np.concatenate((np.zeros(len(test1)),np.ones(len(test2))))

file1 = open('Task1.txt', 'w+', encoding='utf-8')
file1.write("Multinomial Naive Bayes results : ---------- \n")

tempar = [1, 10, 100, 1000, 10000]


def tokenize(content):

    listwords = word_tokenize(content)
    listwords = [word.lower() for word in listwords]
    punc_table = str.maketrans('', '', '\t')
    listwords = [word.translate(punc_table) for word in listwords]
    stoppers = set(stopwords.words('english'))
    listwords = [word for word in listwords if word not in stoppers]
    listwords = [lemma.lemmatize(word) for word in listwords]
    return listwords

file3 = open('Task3.txt', 'w+', encoding="utf-8")
file3.write("KNN : ----\n")
tempar2 = [1, 10, 50]
for i in tempar2:
    pipe = pipeline.Pipeline([('tfidf_vectorizer', TfidfVectorizer(
        min_df=5, max_df=0.8, tokenizer=tokenize, lowercase=True)), ('kNN_classifier', KNeighborsClassifier(n_neighbors=i))])
    pipe.fit(total1, ar1)
    knn = pipe.predict(total2)
    file3.write(str(f1_score(knn, ar2, average='macro'))+"\n")

file3.close()
