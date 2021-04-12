# encoding: utf-8

import os
import pickle
import numpy as np
import lightgbm as lgb

# from .preprocess import split2
# from functools import partial
from scipy.sparse import csr_matrix
# from sklearn.feature_extraction.text import TfidfVectorizer


path = os.path.dirname(__file__)


# with open(os.path.join(path, 'model/ads-detect-1-20200125.emb'), 'rb') as f:
# 	vectorizer = pickle.load(f)


# with open(os.path.join(path, 'model/ads-detect-1-20200125.feature_names'), 'rb') as f:
#     feature_names = pickle.load(f)
# 
# 
# with open(os.path.join(path, 'model/ads-detect-1-20200125.vocab'), 'rb') as f:
#     vocabulary = pickle.load(f)
# 
# 
# vectorizer = TfidfVectorizer(sublinear_tf=True,
#     vocabulary=vocabulary,
#     tokenizer=partial(split2, feature_names))


from .train import vectorizer


bst = lgb.Booster(model_file=os.path.join(path, 'model/ads-detect-1-20200125.mdl'))


def predict(X):
	X = np.array(X)
	X_length = np.array([[len(i) for i in X]]).T
	X = vectorizer.transform(X).toarray()

	print(X.shape)
	print(X_length.shape)

	X = csr_matrix(np.concatenate((X, X_length), axis=1))
	
	y_pred = bst.predict(X)
	y_pred = np.where(y_pred > 0.5, 1, -1)

	return y_pred.tolist()



if __name__ == '__main__':

	X = ['霸服军团收吴，魏，蜀国活人，来的加 1979574312私聊',
		 '你好 你这个号打算卖吗',
		 '岀赀縁 masonghe86']

	y_pred = predict(X)

	print(y_pred)
