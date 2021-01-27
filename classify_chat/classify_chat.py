# encoding: utf-8

import pickle
import numpy as np
import lightgbm as lgb

from scipy.sparse import csr_matrix


with open('./model/ads-detect-1-20200125.emb', 'rb') as f:
	vectorizer = pickle.load(f)


bst = lgb.Booster(model_file='./model/ads-detect-1-20200125.mdl')


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
