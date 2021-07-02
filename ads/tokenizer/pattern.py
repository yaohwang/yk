# encoding: utf-8

import re
import textwrap

from typing import List, Tuple


special = [ 
    '[LOC]',
    '[EMJ]',
    '[NUM]-1', '[NUM]-2', '[NUM]-3', '[NUM]-4', '[NUM]-5', '[NUM]-6', '[NUM]-7',
    '[ABU]',
    '[CTA-M]', '[CTA]',
    '[TRS]',
    '[RES]', '[RES-S]',
    '[VIP]',
    '[WHO]',
    '[PLG]',
    '[OGM]',
    '[MNY]',
    '[URL]',
    '[AUD]',
]


""" base
"""

_pattern_num_base = '0-9零一二三四五六七八九'
_pattern_num = '%s十百千万亿' % _pattern_num_base

_pattern_char = 'a-zA-Z_'
_pattern_location = '\{localization:\d{1,3}\-\d{1,3}\}'

_pattern_emoji_1 = 'biaoqingqxfz_321445821:[0-9]{1,3}'
_pattern_emoji_2 = 'chatemoji:\d{1,2}'

_pattern_contact_charnum = '[a-z0-9\*\-_:]{6,}'
_pattern_contact_char = '[a-z\*\-_:]{5,}'

_pattern_punctuation = '`~!@#\$%\^&\*\(\)_\-=\[\]\{\}\|\\;:\'",<\.>\?/' \
                       '·~！@#￥%……&*（）——\-=【】\{\}|、；：「『，。《》、？' \
                       '\s'


""" global
"""

def pattern_full(pattern: str) -> str:
    return '^%s$' % pattern


pattern_full_defense = '^防守\[.*\].*的进攻:防守\*.*\*.*的进攻$'
pattern_full_attack1 = '^进攻了\[.*\].*:进攻了\*.*\*.*$'
pattern_full_attack2 = '^进攻了[0-9]{1,2}级.*:进攻了[0-9]{1,2}级.*$'
pattern_full_attack3 = '^进攻了.{1,5}[县村]:进攻了.{1,5}[县村]$'

pattern_full_url = '^http[s\\*]{1}://[a-z0-9\\./\\*\-]{1,}$'
pattern_full_audio = '^{audio:https://qxfzios\-cdn\-hz\.himengyou\.com/\d{4}-\d{2}-\d{2}/\d{4}.(?:mp3|amr)=\d{1}\}$'

pattern_full_systeminfo = '(%s)' % '|'.join([
    pattern_full_defense,
    pattern_full_attack1,
    pattern_full_attack2,
    pattern_full_attack3,
])


def find_systeminfo(subtext: str) -> List[str]:
    m = re.match(pattern_full_systeminfo, subtext)
    return None if not m else ['[SYS]']


def find_audio(subtext: str) -> List[str]:
    m = re.match(pattern_full_audio, subtext)
    return None if not m else ['[AUD]']


def find_url(subtext: str) -> List[str]:
    m = re.match(pattern_full_url, subtext)
    return None if not m else ['[URL]']



""" valid
"""

pattern_valid_email = 'theme:(.*)content:(.*)'
pattern_valid_schedulemsg = '\{schedulemsg:[0-9]{10}-(.*)\}'


def extract_email(text: str) -> re.Match:
    return re.match(pattern_valid_email, text)


def extract_schedulemsg(text: str) -> re.Match:
    return re.match(pattern_valid_schedulemsg, text)


def remove_duplicates(text: str) -> str:
    if 3 > len(text): return text
    if 1 == len(set(text)): return text[0]
    for i in divisor(len(text)):
        t = textwrap.wrap(text, i)
        if 1 == len(set(t)): return t[0]
    return text


def divisor(i: int) -> List[int]:
    return [_ for _ in range(2, i//2+1) if 0 == i%_]


""" local
"""

def pattern_start(pattern: str) -> str:
    return '^%s' % pattern


pattern_num_0 = '[%s]+' % _pattern_num
pattern_num_1 = '[%s]+[多万|万]{1,}' % _pattern_num
pattern_num_2 = '[%s]+个[%s]+' % (_pattern_num, _pattern_num)
pattern_num_3 = '[%s]+w' % _pattern_num
pattern_num = '(%s)' % '|'.join([ 
    pattern_num_1,
    pattern_num_2,
    pattern_num_3,
    pattern_num_0,
])

pattern_char = '[%s]+' % _pattern_char
pattern_charnum = '[%s%s]+' % (_pattern_char, _pattern_num_base)
pattern_punctuation = '[%s]+' % _pattern_punctuation
pattern_cn = '[^%s%s%s]' % ('0-9', _pattern_char, _pattern_punctuation)

pattern_group = '(%s)' % '|'.join([
    pattern_num_1,
    pattern_num_2,
    pattern_num_3,
    pattern_cn,
    pattern_charnum,
    pattern_num_0,
    pattern_char,
    pattern_punctuation,
])

pattern_start_location = pattern_start(_pattern_location)

pattern_start_contact_charnum = pattern_start(_pattern_contact_charnum)
pattern_start_contact_char = pattern_start(_pattern_contact_char)

pattern_start_num = '(^%s)' % '|'.join([ 
    pattern_num_1,
    pattern_num_2,
    pattern_num_3,
    pattern_num_0,
])

pattern_start_emoji = '(^%s)' % '|'.join([
    _pattern_emoji_1,
    _pattern_emoji_2,
])



def find_all(subtext: str) -> List[str]:
    return zip(*[(_.end(),_.group()) for _ in re.finditer(pattern_group, subtext)])


def find_location(subtext: str) -> Tuple[str, int]:
    m = re.match(pattern_start_location, subtext)
    return (None, -1) if not m else ('[LOC]', m.end())


def find_emoji(subtext: str) -> Tuple[str, int]:
    m = re.match(pattern_start_emoji, subtext)
    return (None, -1) if not m else ('[EMJ]', m.end())


def find_contact_charnum(subtext: str) -> Tuple[str, int]:
    m = re.match(pattern_start_contact_charnum, subtext)
    return (None, -1) if not m else ('[CTA]', m.end())


def find_contact_char(subtext: str) -> Tuple[str, int]:
    m = re.match(pattern_start_contact_char, subtext)
    return (None, -1) if not m else ('[CTA]', m.end())


def find_num(subtext: str) -> Tuple[str, int]:
    m = re.match(pattern_start_num, subtext)
    return (None, -1) if not m else ('[NUM]-%s' % m.end(), m.end())


pattern_full_char = pattern_full(pattern_char)
pattern_full_charnum = pattern_full(pattern_charnum)
pattern_full_punctuation = pattern_full(pattern_punctuation)


def is_char(subtext: str) -> bool:
    return bool(re.match(pattern_full_char, subtext))


def is_charnum(subtext: str) -> bool:
    # need exclude char & num first
    return bool(re.match(pattern_full_charnum, subtext))


def is_punctuation(subtext: str) -> bool:
    return bool(re.match(pattern_full_punctuation, subtext))
