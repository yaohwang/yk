# encoding: utf-8

import dill
import pickle
import numpy as np

from time import time
from sklearn.feature_extraction.text import TfidfVectorizer

# from tokenizer import split2 as split
from dataset import X_train, X_test
# split = list
from tokenizer import tokenize


vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer=tokenize)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

feature_names = vectorizer.get_feature_names()
if feature_names: feature_names = np.asarray(feature_names)

with open('./model/tfidf.mdl', 'wb') as f:
    dill.dump(vectorizer, f)
