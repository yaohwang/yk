# encoding: utf=8

from typing import List


def one_in_text(keys: List[str], x: List[str]) -> bool:
    return bool(set(keys) & set(x))


def all_in_text(keys: List[str], x: List[str]) -> bool:
    return bool((set(keys) & set(x)) == set(keys))


def rule(x: List[str]) -> int:
    if ['[CTA]'] == x \
    or ['[TRS]'] == x \
    or ['[CTA-M]'] == x \
    or ['[RES]'] == x \
    or '广告' in x \
    or (1 == len(x) and x[0].startswith('[NUM]') and int(x[0][6:]) >= 8): 
        return 2


def is_suspect(x: List[str]) -> bool:
    return one_in_text(['v', 'q', '微', '群', '扣', '加', '收'], x) \
        or all_in_text(['企', '鹅'], x) \
        or all_in_text(['兑', '换', '码'], x) \
        or all_in_text(['礼', '包', '码'], x) \
        or all_in_text(['福', '利'], x) \
        or all_in_text(['带', '队'], x)
