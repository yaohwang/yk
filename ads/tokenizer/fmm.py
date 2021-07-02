# encoding: utf-8

import os
import re
import opencc

from typing import List, Callable, Tuple
from .pattern import (
    find_all,
    find_systeminfo,
    find_location,
    find_emoji,
    find_contact_charnum,
    find_contact_char,
    find_num,
    extract_email,
    extract_schedulemsg,
    is_char,
    is_charnum,
    remove_duplicates,
)

from .trie import (
    trie,
    find,
    tree,
)

path_dict = '/data2/wangyh/project/yk/ads/tokenizer/dict'
root = trie(path_dict)
# tree(root)

from .tokenizer_base import normalize


# TODO: stop words
# TODO: drop whitespace or split by it
# TODO: url
# TODO: audio


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
    tokens = full_pattern(text)
    if not tokens: tokens = part_pattern(text)
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
    # text = text.replace('*','')
    text = re.sub('\s', '', text)

    funcs = [
        extract_email,
        extract_schedulemsg,
    ]

    text = extract(funcs, text)

    return text



def full_pattern(text: str) -> List[str]:
    return find_systeminfo(text)


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

    # TODO: merge with _match
    def match(funcs: List[Callable], subtext: str) -> Tuple[str, int]:
        token, length = None, -1
        lengths, chars = find_all(subtext)
        for func in funcs:
            current_token, current_length = func(subtext, chars, lengths)
            # print(func, repr(subtext), chars, lengths, current_token, current_length)
            # if current_token is not None and length < current_length:
            if current_token is not None and 0 < current_length:
                return current_token, current_length
        # print()
        return token, length
            
    funcs = [
        _part_cn,
        _part_charnum,
        _part_char,
        _part_num,
    ]

    token, length = _part(subtext)
    if token is not None and 0 < length:
        return token, length

    return match(funcs, subtext)


def _match(funcs: List[Callable], subtext: str) -> Tuple[str, int]:
    token, length = None, -1
    for func in funcs:
        current_token, current_length = func(subtext)
        # print(func, subtext, current_token, current_length)
        if current_token is not None and 0 < current_length:
            return current_token, current_length
    return token, length


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
    # TODO:
    funcs = [
        find_contact_charnum,
        find_num,
    ]

    base = remove_duplicates(chars[0])
    _subtext = remove_duplicates(chars[0]) if is_charnum(chars[0]) else subtext
    token, length = _match(funcs, _subtext)
    length = len(chars[0]) if is_charnum(chars[0]) else length
    
    return token, length


def _part_char(subtext: str=None, chars: List[str]=None, *args) -> Tuple[str, int]:
    # TODO:
    token, lenght = None, -1

    if is_char(chars[0]):
        token, idx = find(root, chars[0])
        # return token, idx+1
        length = idx+1

    if token is None:
        token, length = find_contact_char(subtext)
    
    return token, length


def _part_num(subtext: str=None, chars: List[str]=None, *args) -> Tuple[str, int]:
    # TODO:
    return None, -1
