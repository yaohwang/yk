# encoding: utf-8

import os

from functools   import partial
from sklearn     import metrics
from .preprocess import *


def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6


path = os.path.dirname(__file__)


data_train = pd.read_excel(os.path.join(path, 'data/dataset_ads-20210113-1-labeled.xlsx'))
data_train = data_train[['label', 'content']]
data_train = data_train.dropna()

print(data_train.shape)
data_train.head(3)


data_test = pd.read_excel(os.path.join(path, 'data/dataset_ads-20210120-1-labeled.xlsx'))
data_test = data_test[['label', 'content']]
data_test.head(3)


data_train.loc[data_train.label.isin([1, 9, 24]), 'label'] = -1   # ads
data_train.loc[~(data_train.label==-1), 'label'] = 1

data_train.label.value_counts(normalize=True)


data_test.loc[data_test.label.isin([1, 9, 24]), 'label'] = -1
data_test.loc[~(data_test.label==-1), 'label'] = 1
data_test.label.value_counts(normalize=True)


X_train, X_test = data_train.content, data_test.content
y_train, y_test = data_train.label.tolist(), data_test.label.tolist()


data_train_size_mb = size_mb(X_train)
data_test_size_mb = size_mb(X_test)

print("%d documents - %0.3fMB (training set)" % (len(X_train), data_train_size_mb))
print("%d documents - %0.3fMB (test set)" % (len(X_test), data_test_size_mb))
print()


""" vocab
"""

print("Extracting features from the training data using a sparse vectorizer")

t0 = time()

vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=1e-3, tokenizer=split1)
tfidf = vectorizer.fit_transform(X_train)
        
duration = time() - t0

print("done in %fs at %0.3fMB/s" % (duration, data_train_size_mb / duration))
print("n_samples: %d, n_features: %d" % tfidf.shape)
print()

feature_names = vectorizer.get_feature_names()

# with open('./model/ads-detect-1-20200125.feature_names', 'wb') as f:
#     pickle.dump(feature_names, f)


""" feature
"""

print("Extracting features from the training data using a sparse vectorizer")

t0 = time()

vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer=partial(split2, feature_names))
X_train = vectorizer.fit_transform(X_train)
    
    
duration = time() - t0

print("done in %fs at %0.3fMB/s" % (duration, data_train_size_mb / duration))
print("n_samples: %d, n_features: %d" % X_train.shape)
print()


print("Extracting features from the test data using the same vectorizer")

t0 = time()
X_test = vectorizer.transform(X_test)
duration = time() - t0

print("done in %fs at %0.3fMB/s" % (duration, data_test_size_mb / duration))
print("n_samples: %d, n_features: %d" % X_test.shape)
print()


# with open('./model/ads-detect-1-20200125.emb', 'wb') as f:
#     pickle.dump(vectorizer, f)
# 
# with open('./model/ads-detect-1-20200125.vocab', 'wb') as f:
#     pickle.dump(vectorizer.vocabulary_, f)


# if feature_names: feature_names = np.asarray(feature_names)
# 
# 
# """ train
# """
# 
# param = {'num_leaves': 2**5-1, 'objective': 'binary'}
# param['metric'] = 'auc'
# 
# num_round = 1000
# 
# length = np.expand_dims(data_train['content'].apply(len).to_numpy(), axis=1)
# print(X_train.shape)
# print(length.shape)
# X_train = csr_matrix(np.concatenate((X_train.toarray(), length), axis=1))
# X_train.shape
# 
# 
# length = np.expand_dims(data_test['content'].apply(len).to_numpy(), axis=1)
# print(X_test.shape)
# print(length.shape)
# X_test = csr_matrix(np.concatenate((X_test.toarray(), length), axis=1))
# X_test.shape
# 
# train_data = lgb.Dataset(X_train, label=y_train)
# bst = lgb.train(param, train_data, num_round)
# 
# y_pred = bst.predict(X_test)
# y_pred = np.where(y_pred > 0.5, 1, -1)
# 
# 
# print(metrics.classification_report(y_test, y_pred))
# 
# bst.save_model('./model/ads-detect-1-20200125.mdl')
