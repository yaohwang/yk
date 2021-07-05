# encoding: utf=8

import re

from typing import List

from ..tokenizer import (
    special,
    specialnum,
    special0,
    special1,
    special2,
    tokenize,
)


def rule_predict(tokens: List[str]) -> int:

    if 1 == len(tokens):
        token = tokens[0]
        if token in special0:
            return 0
        elif token in special1:
            return 1
        elif token in special2 \
        or token in ['收', '+', '十']:
            return 2

    elif 2 == len(tokens):
        candi = None

        if tokens[0] in specialnum: candi = tokens[1]
        if tokens[1] in specialnum: candi = tokens[0]
        if candi in special1 or candi in special2:
            return 2

        if '加' == tokens[0]: candi = tokens[1]
        if '加' == tokens[1]: candi = tokens[0]
        if candi in ['已', '如何', '欢迎', special.WHO]:
            return 2

        if special.RES in tokens and '缺' in tokens:
            return 2

    elif 3 == len(tokens):
        if (special.RES in tokens and '缺' in tokens) \
        or (special.WHO in tokens and special.ADD in tokens):
            return 2



def rule_suspect(tokens: List[str]) -> bool:

    def suspect(token: str) -> bool:
        return token in specialnum \
            or token in special1 \
            or token in special2 \
            or token in ['收','送', '领', '缺', '工作室', '挂', '带队']

    for token in tokens:
        if suspect(token):
            return True
    return False


if __name__ == '__main__':
    print(rule_predict(['[NUM]-5', '[RES]']))
    print(rule_predict(['[NUM]-3', '[LOC]']))
    print(rule_predict(['[VIP]', '[NUM]-3']))

    print(rule_predict(tokenize('出')))
    print(rule_predict(tokenize('交易猫')))
