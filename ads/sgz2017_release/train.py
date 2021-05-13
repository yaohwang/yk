# encoding: utf-8

import sys
import dill
import numpy as np
import pandas as pd
import lightgbm as lgb

from time import time
from functools import partial
from optparse import OptionParser
from scipy.sparse import csr_matrix

from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn import metrics

from .feature import X_train, X_test, feature_names
from .dataset import y_train, y_test, data_train, data_test


def fit(clf, X_train, y_train):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)
    return train_time


def predict(clf, X_test):
    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)
    return pred, test_time


def accuracy(y_test, pred):
    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    return score


def print_coef(clf, feature_names):
    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print()


def print_report(y_test, pred):
    print("classification report:")
    print(metrics.classification_report(y_test, pred, digits=3))


def print_cm(y_test, pred):
    print("confusion matrix:")
    print(metrics.confusion_matrix(y_test, pred))


def get_desc(clf):
    return str(clf).split('(')[0]


def __benchmark(X_train, y_train, X_test, y_test, feature_names, clf):
    train_time = fit(clf, X_train, y_train)
    pred, test_time = predict(clf, X_test)
    score = accuracy(y_test, pred)
    clf_descr = get_desc(clf)

    print_coef(clf, feature_names)
    print_report(y_test, pred)
    print_cm(y_test, pred)
    print()
    return pred, clf_descr, score, train_time, test_time


benchmark = partial(__benchmark, X_train, y_train, X_test, y_test, feature_names)


results = []

for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="sag"), "Ridge Classifier"),
        (Perceptron(max_iter=50), "Perceptron"),
        (PassiveAggressiveClassifier(max_iter=50), "Passive-Aggressive"),
        (KNeighborsClassifier(n_neighbors=10), "kNN"),
        (RandomForestClassifier(), "Random forest")):
    print('=' * 80)
    print(name)
    results.append(benchmark(clf))


for penalty in ["l2", "l1"]:
    print('=' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    results.append(benchmark(LinearSVC(penalty=penalty, dual=False, tol=1e-3)))

    # Train SGD model
    results.append(benchmark(SGDClassifier(alpha=.0001, max_iter=50, penalty=penalty)))


# Train SGD with Elastic Net penalty
print('=' * 80)
print("Elastic-Net penalty")
results.append(benchmark(SGDClassifier(alpha=.0001, max_iter=50, penalty="elasticnet")))


# Train NearestCentroid without threshold
print('=' * 80)
print("NearestCentroid (aka Rocchio classifier)")
results.append(benchmark(NearestCentroid()))


# Train sparse Naive Bayes classifiers
print('=' * 80)
print("Naive Bayes")
results.append(benchmark(MultinomialNB(alpha=.01)))
results.append(benchmark(BernoulliNB(alpha=.01)))
results.append(benchmark(ComplementNB(alpha=.1)))


param = {'num_leaves': 2**5-1, 'objective': 'binary'}
param['metric'] = 'auc'

num_round = 1000

length = np.expand_dims(data_train['content'].apply(len).to_numpy(), axis=1)
print(X_train.shape)
print(length.shape)
X_train = csr_matrix(np.concatenate((X_train.toarray(), length), axis=1))

length = np.expand_dims(data_test['content'].apply(len).to_numpy(), axis=1)
print(X_test.shape)
print(length.shape)
X_test = csr_matrix(np.concatenate((X_test.toarray(), length), axis=1))

train_data = lgb.Dataset(X_train, label=y_train)
bst = lgb.train(param, train_data, num_round)

y_pred = bst.predict(X_test)
y_pred = np.where(y_pred > 0.5, 1, -1)

print(metrics.classification_report(y_test, y_pred, digits=3))

bst.save_model('./model/ads-2.mdl')
