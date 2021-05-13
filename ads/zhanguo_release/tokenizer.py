# encoding: utf-8

import re
import jieba

from typing import Union, List


def flatten_once(ll: List[List]):
    return [e for l in ll for e in l]


def valid_head_tail(l: List):
    if not l:
        return l
    if not l[0] and not l[-1]:
        return l[1:-1]
    elif not l[0]:
        return l[1:]
    elif not l[-1]:
        return l[:-1]
    else:
        return l


def split(tokens: List[str], key: str) -> List[str]:
    return flatten_once(_split(token, key) for token in tokens)


def _split(token: str, key: str) -> List[str]:
    return valid_head_tail(re.split('(%s)' % key, token))


def tokenize(text: str) -> List[str]:

    def coarse(text: str) -> List[str]:
        return valid_head_tail(re.split('([0-9]+[多万]{0,}|[a-zA-Z0-9]+)', text))

    def recognize(tokens: Union[str, List[str]]):
        if isinstance(tokens, str):
            return _recognize(tokens)
        elif isinstance(tokens, (list, tuple)):
            return flatten_once(_recognize(token) for token in tokens)
        else:
            raise ValueError(
                f"type of tokens unknown: {type(tokens)}. "
                f"Should be one of a str, list, tuple."
            )

    def _recognize(text: str) -> List[str]:

        def is_special(token: str):
            return token in [
                '[NUM]-1',
                '[NUM]-2',
                '[NUM]-3',
                '[NUM]-4',
                '[NUM]-5',
                '[NUM]-6',
                '[NUM]-7',
                '[ABU]',
                '[CTA-M]',
                '[CTA]',
                '[TRS]',
                '[RES]',
            ]

        def _recognize_num(text: str) -> List[str]:
            if 1 == len(set(text)):
                return ['[NUM]-1']
            elif 8 <= len(text):
                return ['[CTA]']
            return ['[NUM]-%s' % len(text)]

        def _recognize_charnum(text: str) -> List[str]:
            if text in ['cnmlgb', 'cnm', 'nm']: return ['[ABU]']
            elif text in ['v', 'vx', 'q', 'qq']: return ['[CTA-M]']
            elif 'mai' == text: return ['[TRS]']
            elif 'v587' == text: return ['威', '武', '霸', '气']
            elif len(text) > 5: return ['[CTA]']
            else: return list(text)

        def _recognize_other(text: str) -> List[str]:
            keys = ['微信号', '微信', '微', '扣扣', '群']
            tokens = [text]
            for key in keys:
                tokens = split(tokens, key)
                tokens = flatten_once(['[CTA-M]'] if token in keys or is_special(token) else [token] for token in tokens)
            
            keys = ['资源', '玉珏', '玉', '礼包码', '礼包']
            for key in keys:
                tokens = split(tokens, key)
                t = []
                for token in tokens:
                    if is_special(token):
                        t.append(token)
                    elif token in keys:
                        t.append('[RES]')
                    else:
                        t.append(token)
                tokens = t

            words = ['加油', '加速', '加快', '加入', '多少', '广告']

            for word in words:
                tokens = split(tokens, word)

            tokens = flatten_once([[token] if is_special(token) or token in words else list(token) for token in tokens])
            return tokens

        if re.match('[0-9]+[多万]{0,}', text): 
            return _recognize_num(text)
        elif re.match('[a-zA-Z0-9]+', text):
            return _recognize_charnum(text)
        else:
            return _recognize_other(text)

    def stop_words(tokens: List[str]) -> List[str]:
        d = ['了']
        return [token for token in tokens if token not in d]

    tokens = coarse(text.lower())
    tokens = recognize(tokens)
    tokens = stop_words(tokens)

    return tokens


if __name__ == '__main__':
    print(tokenize('0你好v123测试456%&-1'))
    print(tokenize('微信号多少？'))
    print(tokenize('微信多少'))
    print(tokenize('108给3万玉要加扣扣730356479'))
    print(tokenize('加油加油加油'))
    print(tokenize('200多万资源'))
    print(tokenize('资源爆满了'))
