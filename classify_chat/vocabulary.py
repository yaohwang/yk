# encoding: utf-8

import pickle
import pandas as pd

from pathlib import Path
from bisect import bisect
from itertools import chain
from collections import Counter
from tqdm import tqdm
from collections import defaultdict

from unicode import unicode_mapping
from preprocess_v2 import NormalizerSGZChat

from mih import VocabularyBPE

path_data = Path('~/data/yk-sgz2017-chat/').expanduser()
path_to = path_data / 'data-8-20210329'

vocab = VocabularyBPE()
# vocab.create_vocab(path_to, vocab_size=10**4, checkpoint=200)
vocab.create_vocab(vocab.load_vocab('./.vocab/.checkpoint-last-20000'), vocab_size=2.5e4, checkpoint=200)
