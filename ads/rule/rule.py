# encoding: utf=8

import re

from typing import List

from ..tokenizer import (
    special,
    specialnum,
    special0,
    special1,
    special2,
    specialrisk,
    tokenize,
)


def rule_predict(tokens: List[str]) -> int:

    if 1 == len(tokens):
        token = tokens[0]
        if token in special1:
            return 1
        elif (token in special2 and special.RESS != token) \
        or token in ['收', '+', '十']:
            return 2
        elif special.HVN == token:
            return 2
        elif token in special0:
            return 0

    elif 2 == len(tokens):
        candi = None

        if tokens[0] in specialnum: candi = tokens[1]
        if tokens[1] in specialnum: candi = tokens[0]

        if candi == special.WHO:
            return 0
        elif candi in special1 or candi in special2:
            return 2

        if '加' == tokens[0]: candi = tokens[1]
        if '加' == tokens[1]: candi = tokens[0]
        if candi in ['已', '如何', '欢迎', special.WHO]:
            return 2

        if special.ADD in tokens and special.AGR in tokens:
            return 2

        if special.WHO in tokens and special.NEED in tokens:
            return 2

        if special.WHO == tokens[0] and special.HVN == tokens[1]:
            return 2

        if special.RES in tokens \
        and ('缺' in tokens or special.HVN in tokens):
            return 2

        if special.RESS in tokens and special.HVN in tokens:
            return 0

        if special.LOC in tokens \
        and (
            '给' in tokens  \
            or '发' in tokens \
            or special.HVN in tokens
        ):
            return 2

        if '位置' in tokens \
        and (
            '给' in tokens  \
            or '发' in tokens
        ):
            return 2

        if special.MNY in tokens and special.HVN in tokens:
            return 2

    elif 3 == len(tokens):
        if (special.RES in tokens and '缺' in tokens) \
        or (special.WHO in tokens and special.ADD in tokens):
            return 2

        if (special.RESS in tokens and special.HVN in tokens and special.WHO in tokens):
            return 0

    if special.ADD in tokens:
        if ('团' in tokens or '团长' in tokens):
            if not bool(set(specialrisk) & set(tokens)):
                return 0
        # elif special.CTA in tokens or special.CTAM in tokens:
        #     return 2



def rule_suspect(tokens: List[str]) -> bool:

    def suspect(token: str) -> bool:
        return token in specialnum \
            or token in special1 \
            or token in special2 \
            or token in ['收','送', '领', '缺', '工作室', '挂', '带队', '+', '广告'] \
            or token == special.HVN

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
