# encoding: utf-8

import numpy as np
import pandas as pd

from tqdm import tqdm
from pathlib import Path
from collections import Counter

from typing import (
    List,
    Union,
)

from .data import load
from .service import predict
from .rule import rule
from .tokenizer import tokenize


# path = Path('~/data/yk-zhanguo-chat/tw').expanduser()
path = Path('~/data/yk-zhanguo-chat/dl').expanduser()
path

df = load(path, columns='chat_content')
df = df.dropna()
df.head(3)

%time df['predict'] = predict(df['chat_content'].tolist(), verbose=True)

df.shape

df = df.drop_duplicates()
df.shape

df = df.value_counts()
df.name = 'cnt'
df = df.reset_index()
df.shape

df[df.cnt > 3].shape

df.cnt.sum()

df[df.cnt > 3]['cnt'].sum()
df[df.cnt > 3]['cnt'].sum() / df.cnt.sum()
df[df.cnt > 2]['cnt'].sum() / df.cnt.sum()
df[df.cnt > 1]['cnt'].sum() / df.cnt.sum()

#df_ = df[df.cnt > 2]
df_ = df[df.cnt > 1]
df_ = df_.drop(columns='cnt')
df_ = df_.rename(columns={'chat_content':'text'})

#df_['game'] = 'zhanguo'
#df_['version'] = 1
#df_['region'] = 'tw'

df_['rule'] = df_.text.apply(lambda x: rule(tokenize(x), x))
df_ = df_[df_.rule.isna()]
df_ = df_.drop(columns='rule')


# name = 'dl-20210609-1.csv'
name = 'dl-20210615-1.csv'

# df_.to_csv(path.parent/'tw-20210423-1.csv', encoding='utf-8', index=False)
# df_.to_csv(path.parent/'dl-20210430-1.csv', encoding='utf-8', index=False)
# df_.to_csv(path.parent/'dl-20210604-1.csv', encoding='utf-8', index=False)
df_.to_csv(path.parent/name, encoding='utf-8', index=False)


df_ = df[df.cnt == 1]
df_ = df_.drop(columns='cnt')
df_ = df_.rename(columns={'chat_content':'text'})


df_['rule'] = df_.text.apply(lambda x: rule(tokenize(x), x))

df_ = df_[df_.rule.isna()]

# name = 'dl-20210609-2.csv'
name = 'dl-20210615-2.csv'

# df_.to_csv(path.parent/'dl-20210430-2.csv', encoding='utf-8', index=False)
# df_.to_csv(path.parent/'dl-20210604-2.csv', encoding='utf-8', index=False)
df_.to_csv(path.parent/name, encoding='utf-8', index=False)
