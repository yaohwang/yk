# encoding: utf-8

import jieba

from typing import List, Any

Model = Any


def predict(
    model: Model,
    texts: List[str],
) -> List[int]:

    def preprocess(text: str) -> str:
        return ' '.join(jieba.cut(text))

    def _predict(text: str) -> int:
        # TODO: predict batch
        x = preprocess(text)
        y_pred = model.predict([x])
        y_pred = int(float(y_pred[0][0][0].split('__label__')[-1]))
        return y_pred

    return [_predict(text) for text in texts]
