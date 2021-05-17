# encoding: utf-8

import os
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split


def load(path_data, rename_columns={}):
    data = pd.read_excel(path_data)
    if rename_columns: data = data.rename(columns=rename_columns)
    data = data.dropna()
    data.label = data.label.astype(int)
    data.content = data.content.astype(str)
    # print(f'data: {data.shape}')
    # print(data['label'].value_counts())
    return data


def split(data):
    X, y = data['content'], data['label']
    X = X.tolist()
    y = y.tolist()
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)
    # print(X_train.shape)
    # print(len(y_train))
    # print(y_train.value_counts())
    # print(X_test.shape)
    # print(len(y_test))
    # print(y_test.value_counts())
    return X_train, X_test, y_train, y_test


path_root = Path('~/data/yk-zhanguo-chat').expanduser()

# path_data = path_root / 'dl-20210430-1-labeled.xlsx'
# columns={'text':'content', 'predict':'label'}
# data = load(path_data, rename_columns=columns)
# X_train, X_test, y_train, y_test = split(data)

path_data = path_root / 'dl-20210430-1-labeled.xlsx'
columns={'text':'content', 'predict':'label'}
data = load(path_data, rename_columns=columns)
X_test = data['content'].tolist()
y_test = data['label'].tolist()

path_data = path_root / 'dl.sgz2017-20210513-1-labeled.xlsx'
data = load(path_data)
X_train = data['content'].tolist()
y_train = data['label'].tolist()
