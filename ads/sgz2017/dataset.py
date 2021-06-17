# encoding: utf-8

import os
import pandas as pd

path = os.path.dirname(__file__)

data_train_1 = pd.read_excel(os.path.join(path,'data/train-1.xlsx'))
data_train_1 = data_train_1[['label', 'content']]
data_train_1 = data_train_1.dropna()

data_train_2 = pd.read_excel(os.path.join(path,'./data/train-2.xlsx'))
data_train_2 = data_train_2.rename(columns={'text':'content', 'sentiment':'label'}) 
data_train_2 = data_train_2[['label', 'content']]
data_train_2 = data_train_2.dropna()

data_test = pd.read_excel(os.path.join(path,'./data/test-1.xlsx'))
data_test = data_test[['label', 'content']]
data_test.head(3)


data_train_1.loc[data_train_1.label.isin([1, 9, 24]), 'label'] = -1   # ads
data_train_1.loc[~(data_train_1.label==-1), 'label'] = 1
data_train_1.label.value_counts(normalize=True)

data_train_2.loc[data_train_2.label.str.startswith('非广告'), 'label'] = 1
data_train_2.loc[~(data_train_2.label==1), 'label'] = -1    # ads

data_train = pd.concat([data_train_1, data_train_2], axis=0)
data_train.label = data_train.label.astype(int)
data_train.content = data_train.content.astype(str)
data_train.shape

data_test.loc[data_test.label.isin([1, 9, 24]), 'label'] = -1
data_test.loc[~(data_test.label==-1), 'label'] = 1
data_test.label.value_counts(normalize=True)

X_train, X_test = data_train.content, data_test.content
y_train, y_test = data_train.label.tolist(), data_test.label.tolist()

print(len(X_train))
print(len(y_train))
print(len(X_test))
print(len(y_test))
