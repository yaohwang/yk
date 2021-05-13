# encoding: utf-8

import os
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split

path_root = Path('~/data/yk-zhanguo-chat').expanduser()
path_data = path_root / 'dl-20210430-1-labeled.xlsx'

# load
data = pd.read_excel(path_data)
data = data.rename(columns={'text':'content', 'predict':'label'})
data = data.dropna()
data.label = data.label.astype(int)
data.content = data.content.astype(str)
# print(f'data: {data.shape}')
# print(data['label'].value_counts())

# train & test
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
