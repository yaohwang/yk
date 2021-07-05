# encoding: utf-8

import os
import dill
import traceback
import numpy as np
import lightgbm as lgb

from pathlib import Path
from typing import Optional, Any, List, Tuple

from .rule import rule_predict, rule_suspect
from .tokenizer import tokenize

Model = Any
ModelEmbedding = Any


def load_model(
    save_directory: str,
    filename_prefix: Optional[str] = None
) -> Tuple[ModelEmbedding, Model]:
    try:
        path = Path(save_directory)
        filename_prefix = filename_prefix if filename_prefix else 'last'
        name = 'ads-%s.mdl' % filename_prefix
        model_file=(path/name).as_posix()
        model = lgb.Booster(model_file=model_file)
        name = 'embedding-%s.mdl' % filename_prefix
        with (path/name).open('rb') as f:
            model_embedding = dill.load(f)
        return model_embedding, model
    except:
        traceback.print_exc()
        return None, None


path_root = os.path.dirname(__file__)
path_model = Path(path_root) / 'model'
model_embedding_1, model_1 = load_model(path_model, filename_prefix='1-last')
model_embedding_2, model_2 = load_model(path_model, filename_prefix='2-last')


def predict(
    X: List[str],
    model_embedding_1: ModelEmbedding = model_embedding_1,
    model_1: Model = model_1,
    model_embedding_2: ModelEmbedding = model_embedding_2,
    model_2: Model = model_2,
    verbose = False
) -> List[int]:

    def _predict(x: str) -> int:
        tokens = tokenize(x)
        y_pred = rule_predict(tokens)
        if y_pred is None:
            y_pred = predict_model(tokens, model_embedding_1, model_1) if rule_suspect(tokens) else predict_model(tokens, model_embedding_2, model_2)
        return y_pred

    def predict_model(x: str, model_embedding: ModelEmbedding, model: Model) -> int:
        x = model_embedding.transform([x])
        y_pred = model.predict(x)
        y_pred = np.argmax(y_pred, axis=1)[0]
        return y_pred

    if verbose:
        from tqdm import tqdm
        X = tqdm(X)
    return [_predict(x) for x in X]


if __name__ == '__main__':

	X = ['兄弟，来我的军团不',
		 '资源爆满了',
		 '加溦okltgo*同款手u*d就送4020',
         '进攻了4级蛮族:进攻了4级蛮族']

	y_pred = predict(X)
	print(y_pred)
