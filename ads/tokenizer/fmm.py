# encoding: utf-8

import os
import re
import opencc

from pathlib import Path
from typing import List, Callable, Tuple

from .pattern import (
    find_all,
    find_systeminfo,
    find_audio,
    find_url,
    find_location,
    find_emoji,
    find_contact_charnum,
    find_contact_char,
    find_num,
    extract_email,
    extract_schedulemsg,
    is_char,
    is_charnum,
    is_punctuation,
    remove_duplicates,
    special,
)

from .trie import (
    trie,
    find,
    tree,
    has,
)

from .base import normalize


path_root = Path(os.path.dirname(__file__))
path_dict = path_root/'dict'
path_dict_stopwords = path_root/'dict_stopwords'
root = trie(path_dict)
root_stopwords = trie(path_dict_stopwords)


def verbose(func: Callable) -> Callable:

    def inner(text: str) -> List[str]:
        print('text:', text)
        tokens = func(text)
        print('tokens:', tokens)
        print()
        return tokens

    return inner


@verbose
def tokenize(text: str) -> List[str]:
    text = preprocess(text)
    tokens,  = full_pattern(text)
    if not tokens: tokens = part_pattern(text)
    tokens = postprocess(tokens)
    return tokens


cc = opencc.OpenCC('tw2s')


def preprocess(text: str) -> str:

    def extract(funcs: List[Callable], text: str) -> str:
        for func in funcs:
            r = func(text)
            if r:
                return ' '.join(r.groups())
        return text

    text = text.lower()
    text = cc.convert(text)
    text = normalize(text)
    text = re.sub('\s', '', text)

    funcs = [
        extract_email,
        extract_schedulemsg,
    ]

    text = extract(funcs, text)

    return text


def _match(funcs: List[Callable], *args) -> Tuple[str, int]:
    for func in funcs:
        r = func(*args)
        if r[0]:
            return r
    return r


def full_pattern(text: str) -> List[str]:

    funcs = [
        find_systeminfo,
        find_audio,
        find_url,
    ]

    return _match(funcs, text)


def part_pattern(text: str) -> List[str]:
    tokens = []
    i = 0
    while(i < len(text)):
        token, length = _part_pattern(text[i:])
        if -1 == length or 0 == length:
            token = text[i]
            length = 1
        tokens.append(token)
        i += length
    return tokens


def _part_pattern(subtext: str) -> Tuple[str, int]:
            
    funcs = [
        _part_cn,
        _part_charnum,
        _part_char,
        _part_num,
    ]

    token, length = _part(subtext)
    if token is not None and 0 < length:
        return token, length

    chars, lengths = find_all(subtext)
    return _match(funcs, subtext, chars, lengths)


def _part(subtext: str) -> Tuple[str, int]:
    funcs = [
        find_location,
        find_emoji,
    ]
    return _match(funcs, subtext)


def _part_cn(subtext: str=None, chars: List[str]=None, lengths: List[int]=[]) -> Tuple[str, int]:
    token, lenght = None, -1

    token, idx = find(root, chars)
    length = -1 if token is None else lengths[idx]

    if token is None and is_char(chars[0]):
        token, idx = find(root, chars[0])
        length = idx+1

    return token, length


def _part_charnum(subtext: str=None, chars: List[str]=None, *args) -> Tuple[str, int]:
    funcs = [
        find_contact_charnum,
        find_num,
    ]

    base = remove_duplicates(chars[0])
    _subtext = remove_duplicates(chars[0]) if is_charnum(chars[0]) else subtext

    token, idx = find(root, _subtext)
    length = idx+1

    if token is None:
        token, length = _match(funcs, _subtext)
        length = len(chars[0]) if is_charnum(chars[0]) else length

    return token, length


def _part_char(subtext: str=None, chars: List[str]=None, *args) -> Tuple[str, int]:
    token, lenght = None, -1

    if is_char(chars[0]):
        token, idx = find(root, chars[0])
        length = idx+1

    if token is None:
        token, length = find_contact_char(subtext)
    
    return token, length


def _part_num(subtext: str=None, chars: List[str]=None, *args) -> Tuple[str, int]:
    return None, -1


def postprocess(tokens: List[str]) -> List[str]:
    # merge single char or num
    cache = []
    final = []
    for token in tokens:
        if token in special or not is_charnum(token) or 1 < len(token):
            if 1 == len(cache):
                final.append(cache)
            elif 1 < len(cache):
                final.append(''.join(cache))
            final.append(token)
            cache = []
        else:
            cache.append(token)
    if cache: final.append(''.join(cache))
    # drop stop words
    final = [token for token in final if not has(root_stopwords, token) and not is_punctuation(token)]
    return final
