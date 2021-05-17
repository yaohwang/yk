# encoding: utf=8

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
    return '[RES]' in x

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


def rule(x: List[str]) -> int:
    if ['[CTA]'] == x \
    or ['[TRS]'] == x \
    or ['[CTA-M]'] == x \
    or ['[RES]'] == x \
    or (2 == len(x) and has_num(x) and has_resource(x)) \
    or (2 == len(x) and has_num(x) and has_location(x)) \
    or (2 == len(x) and has_num(x) and has_vip(x)) \
    or (2 == len(x) and has_num(x) and has_add(x)) \
    or (2 == len(set(x)) and has_who(x) and has_add(x)) \
    or (2 == len(set(x)) and has_who(x) and has_recruit(x)) \
    or ['收'] == x \
    or ['加'] == x \
    or ['出'] == x \
    or (1 == len(x) and x[0].startswith('[NUM]') and int(x[0][6:]) >= 8): 
    # or '广告' in x \
        return 2


def is_suspect(x: List[str]) -> bool:
    return has_num(x) \
        or has_contact(x) \
        or has_resource(x) \
        or has_account(x) \
        or one_in_text(['v', 'q', '微', '群', '扣', '加', '收', '出', '岀','送', '领'], x) \
        or all_in_text(['企', '鹅'], x) \
        or all_in_text(['兑', '换', '码'], x) \
        or all_in_text(['礼', '包', '码'], x) \
        or all_in_text(['福', '利'], x) \
        or all_in_text(['带', '队'], x)


if __name__ == '__main__':
    print(rule(['[NUM]-5', '[RES]']))
    print(rule(['[NUM]-3', '[LOC]']))
    print(rule(['[VIP]', '[NUM]-3']))

    print(is_suspect(['岀', '赀', '縁', '[CTA]']))
    # print(one_in_text(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领'], ['岀', '赀', '縁', '[CTA]']))
    # print(set(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领']))
    # print(set(['岀', '赀', '縁', '[CTA]']))
    # print(set(['v', 'q', '微', '群', '扣', '加', '收', '出', '送', '领']) & set(['岀', '赀', '縁', '[CTA]']))
