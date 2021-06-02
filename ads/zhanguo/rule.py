# encoding: utf=8

import re

from typing import List


def one_in_text(keys: List[str], x: List[str]) -> bool:
    # return bool(set(keys) & set(x))
    for k in keys:
        if k in x: return True
    return False

def all_in_text(keys: List[str], x: List[str]) -> bool:
    # return bool((set(keys) & set(x)) == set(keys))
    for k in keys:
        if k not in x: return False
    return True

def has_num(x: List[str]) -> bool:
    for _ in x:
        if _.startswith('[NUM]'): return True
    return False

def has_resource(x: List[str]) -> bool:
    return '[RES]' in x \
        or '[RES-S]' in x

def has_location(x: List[str]) -> bool:
    return '[LOC]' in x

def has_vip(x: List[str]) -> bool:
    return '[VIP]' in x

def has_add(x: List[str]) -> bool:
    return '加' in x

def has_who(x: List[str]) -> bool:
    return '[WHO]' in x

def has_recruit(x: List[str]) -> bool:
    return '收' in x

def has_contact(x: List[str]) -> bool:
    return '[CTA]' in x \
        or '[CTA-M]' in x \
        or '私' in x \
        or '聊' in x

def has_account(x: List[str]) -> bool:
    return '号' in x

def has_plugin(x: List[str]) -> bool:
    return '[PLG]' in x

def has_game_other(x: List[str]) -> bool:
    return '[OGM]' in x

def has_money(x: List[str]) -> bool:
    return '[MNY]' in x


def rule(tokens: List[str], x: str) -> int:
    pattern_defense = '^防守\[.*\].*的进攻:防守\*.*\*.*的进攻$'
    pattern_attack = '^进攻了\[.*\].*:进攻了\*.*\*.*$'

    if re.match(pattern_defense, x) \
    or re.match(pattern_attack, x):
        return 0

    pattern_url = '^http[s\\*]{1}://[a-z0-9\\./\\*\-]{1,}$'
    pattern_contact = '^[a-z0-9\s\*\-:]{8,}$'
    pattern_add = '^\+$'

    if re.match(pattern_url, x) \
    or re.match(pattern_add, x):
    # or re.match(pattern_contact, x):
        return 2

    if ['[OGM]'] == tokens \
    or '交易猫' in tokens:
        return 1

    if ['[CTA]'] == tokens \
    or ['[TRS]'] == tokens \
    or ['[CTA-M]'] == tokens \
    or ['[RES]'] == tokens \
    or (2 == len(tokens) and has_num(tokens) and has_resource(tokens)) \
    or (2 == len(tokens) and has_num(tokens) and has_location(tokens)) \
    or (2 == len(tokens) and has_num(tokens) and has_vip(tokens)) \
    or (2 == len(tokens) and has_num(tokens) and has_add(tokens)) \
    or (2 == len(set(tokens)) and has_who(tokens) and has_add(tokens)) \
    or ['收'] == tokens \
    or ['加'] == tokens \
    or ['已', '加'] == tokens \
    or ['如何', '加'] == tokens \
    or ['出'] == tokens \
    or ['号'] == tokens \
    or ['欢迎', '加'] == tokens \
    or ['欢迎', '[WHO]', '加'] == tokens \
    or ['q'] == tokens \
    or ['+'] == tokens \
    or ['十'] == tokens \
    or ['缺', '[RES]'] == tokens \
    or ['有', '缺', '[RES]'] == tokens \
    or ['不', '缺', '[RES]'] == tokens \
    or ['看', '私'] == tokens \
    or ['买'] == tokens \
    or ['[VIP]'] == tokens \
    or (1 == len(tokens) and tokens[0].startswith('[NUM]') and int(tokens[0][6:]) >= 8): 
    # or (2 == len(set(tokens)) and has_who(tokens) and has_recruit(tokens)) \
    # or '广告' in tokens \
        return 2

    if ['收', '[WHO]'] == tokens:
        return 0



def is_suspect(x: List[str]) -> bool:
    return has_num(x) \
        or has_contact(x) \
        or has_resource(x) \
        or has_account(x) \
        or has_plugin(x) \
        or has_game_other(x) \
        or has_money(x) \
        or has_vip(x) \
        or one_in_text(['v', 'q', '微', '群', '扣', '加', '收', '出', '岀','送', '领', '缺', '工作室', '买', '钱', '挂'], x) \
        or all_in_text(['企', '鹅'], x) \
        or all_in_text(['兑', '换', '码'], x) \
        or all_in_text(['礼', '包', '码'], x) \
        or all_in_text(['福', '利'], x) \
        or all_in_text(['带', '队'], x) \
        or all_in_text(['资', '源'], x)


if __name__ == '__main__':
    # print(rule(['[NUM]-5', '[RES]']))
    # print(rule(['[NUM]-3', '[LOC]']))
    # print(rule(['[VIP]', '[NUM]-3']))
    print(rule(['出'], '出'))
    print(rule(['交易猫'], '交易猫'))

    # print(is_suspect(['岀', '赀', '縁', '[CTA]']))
    # print(one_in_text(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领'], ['岀', '赀', '縁', '[CTA]']))
    # print(set(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领']))
    # print(set(['岀', '赀', '縁', '[CTA]']))
    # print(set(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领']) & set(['岀', '赀', '縁', '[CTA]']))
