# encoding: utf-8

import re
import jieba

from typing import Union, List
from tokenizer_base import normalize


special = [
    '[LOC]',
    '[EMJ]',
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
    '[VIP]',
    '[WHO]',
]

words = [
    '下线',
    '加油',
    '加速',
    '加快',
    '加入',
    '多少',
    '广告',
    '军团',
    '团长',
    '有没有',
    # '没有',
    '收到',
    '什么',
    '功勋',
    '怎么',
    '弃坑',
    '收人',
    '进攻',
    '您好',
    '出来',
    '第一',
    '联盟',
    '兄弟',
    '机器人',
    '攻略',
    '红手指',
    '交易猫',
]

words_stop = ['了', '的', '啊', '吗', '吧', '呢']
words_contact_method = ['微信号', '微信', '微', '扣扣', '群', '企鹅', '好友']
words_resource = ['资源', '玉珏', '玉', '礼包码', '礼包', '兑换码', '福利码', '福利', '码', '金', '木', '铁', '石']
words_location = ['光源村', '白鹿村', '白阳村']
words_who = ['您', '你', '我', '他', '你们', '我们', '他们']

words += words_location
words += words_who

single = special + words


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

    def clean(text: str) -> str:
        text = text.replace('*','')
        # text = re.sub('\s', '', text)
        return text

    def replace(text: str) -> str:
        text = _replace(text, 'ziyuan', '资源')

        text = _replace(text, '亻言', '信')

        text = _replace(
            text, 
            [
                '威',
                '徽',
                '徵',
                '微新',
                '微信',
                '魏心',
                '巍信',
                '∨x',
                '∨',
                '؆',
            ], 
            '微'
        )

        text = _replace(
            text,
            [
                '裙',
                '君羊',
            ],
            '群'
        )

        text = _replace(
            text,
            [
                '加一下',
                '加下',
                '加入',
                '咖',
                '架',
                '嫁',
                '十',
                '茄',
                '迦',
            ],
            '加'
        )

        text = _replace(
            text,
            [
                'selling',
                '销售',
                '出售',
                '售',
                '础',
                '岀',
                '麦',
                '卖',
            ],
            '出'
        )

        return text

    def _replace(text: str, from_strs: Union[str, List[str]], to_str: str) -> str:
        if isinstance(from_strs, str):
            return _replace_once(text, from_strs, to_str)
        elif isinstance(from_strs, (list, tuple)):
            for f in from_strs:
                text = _replace_once(text, f, to_str)
            return text
        else:    
            raise ValueError(
                f"type of from_strs unknown: {type(from_strs)}. "
                f"Should be one of a str, list, tuple."
            )

    def _replace_once(text: str, from_str: str, to_str: str) -> str:
        return text.replace(from_str, to_str)

    pattern_email = 'theme:(.*)content:(.*)'
    pattern_schedulemsg = '\{schedulemsg:[0-9]{10}-(.*)\}'

    def extract(text: str) -> str:
        r = re.match(pattern_email, text)
        if r: return ''.join(r.groups())
        r = re.match(pattern_schedulemsg, text)
        if r: return ''.join(r.groups())
        return text


    pattern_num = '0-9零一二三四五六七八九十百千万亿'
    pattern_location = '\{localization:[%s]{1,3}\-[%s]{1,3}\}' % (pattern_num, pattern_num)
    pattern_emoji = 'chatemoji:[%s]{1,2}' % pattern_num
    pattern_num1 = '[%s]+[多万]{1,}' % pattern_num
    pattern_num2 = '[%s]+个[%s]+' % (pattern_num, pattern_num)
    pattern_num3 = '[%s]+w' % pattern_num
    pattern_num0 = '[%s]+' % pattern_num
    pattern_vip = 'vip'
    pattern_charnum = '[a-zA-Z%s]+' % pattern_num

    pattern_tokens = '(%s)' % '|'.join([
        pattern_location,
        pattern_emoji,
        pattern_num1,
        pattern_num2,
        pattern_num3,
        pattern_num0,
        pattern_vip,
        pattern_charnum,
    ])

    def coarse(text: str) -> List[str]:
        return valid_head_tail(re.split(pattern_tokens, text))

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

    def is_special(token: str) -> bool:
        return token in special

    def is_single(token: str) -> bool:
        return token in single

    def is_normal(token: str) -> bool:
        return is_location(token) \
            or is_emoji(token) \
            or is_vip(token)

    def is_location(token: str) -> bool:
        return re.match(pattern_location, token) \
            or token in words_location

    def is_emoji(token: str) -> bool:
        return re.match(pattern_emoji, token)

    def is_vip(token: str) -> bool:
        return re.match(pattern_vip, token)

    def is_num(token: str) -> bool:
        return re.match(pattern_num1, token) \
            or re.match(pattern_num2, token) \
            or re.match(pattern_num3, token) \
            or re.match(pattern_num0, token)

    def is_charnum(token: str) -> bool:
        return re.match(pattern_charnum, token)

    def is_who(token: str) -> bool:
        return token in words_who

    def _recognize(text: str) -> List[str]:

        def _recognize_normal(text: str) -> List[str]:
            if is_location(text): return ['[LOC]']
            elif is_emoji(text): return ['[EMJ]']
            elif is_vip(text): return ['[VIP]']
            elif is_who(text): return ['[WHO]']
            return [text]

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

            def _recognize_contact_method(tokens: List[str]) -> List[str]:
                for word in words_contact_method:
                    tokens = split(tokens, word)
                    tokens = flatten_once(['[CTA-M]'] if token in words_contact_method or is_special(token) else [token] for token in tokens)
                return tokens
            
            def _recognize_resource(tokens: List[str]) -> List[str]:
                for word in words_resource:
                    tokens = split(tokens, word)
                    t = []
                    for token in tokens:
                        if is_special(token):
                            t.append(token)
                        elif token in words_resource:
                            t.append('[RES]')
                        else:
                            t.append(token)
                    tokens = t
                return tokens

            def _recognize_words(tokens: List[str]) -> List[str]:
                for word in words:
                    tokens = split(tokens, word)
                return tokens

            tokens = [text]
            tokens = _recognize_contact_method(tokens)
            tokens = _recognize_resource(tokens)
            tokens = _recognize_words(tokens)
            return tokens

        if is_normal(text):
            return _recognize_normal(text)
        elif is_num(text): 
            return _recognize_num(text)
        elif is_charnum(text):
            return _recognize_charnum(text)
        else:
            tokens = _recognize_other(text)
            tokens = flatten_once([_recognize_normal(token) for token in tokens])
            return tokens

    def stop_words(tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in words_stop]

    def to_single(tokens: List[str]) -> List[str]:
        return flatten_once([[token] if is_single(token) else list(token) for token in tokens])

    def remove_whitespace(tokens: List[str]) -> List[str]:
        tokens = [re.sub('\s', '', token) for token in tokens]
        tokens = [token for token in tokens if token]
        return tokens

    text = text.lower()
    text = normalize(text)
    text = clean(text)
    text = replace(text)
    text = extract(text)

    tokens = coarse(text)
    tokens = recognize(tokens)
    tokens = to_single(tokens)
    tokens = stop_words(tokens)
    tokens = remove_whitespace(tokens)

    return tokens


if __name__ == '__main__':
    print(tokenize('0你好v123测试456%&-1'))
    print(tokenize('微信号多少？'))
    print(tokenize('微信多少'))
    print(tokenize('108给3万玉要加扣扣730356479'))
    print(tokenize('加油加油加油'))
    print(tokenize('200多万资源'))
    print(tokenize('资源爆满了'))
    print(tokenize('chatemoji:7'))
    print(tokenize('Theme:联盟邮件 Content: 进盟的兄弟都加下我微信gj203627，没加下线就当机器人踢了！！加我领礼包码攻略'))
    print(tokenize('企鹅'))
    print(tokenize('*收'))
    print(tokenize('加团长徽：15183063671（梦瑶）我啦你们进群，领取对应的礼包码，不来的当机器人踢了'))
    print(tokenize('Theme:军团消息 Content: 兄弟我盟主，茄我徵NMML87，拉你进盟裙,方便统计活人分配职位，没来的下线当人机踢了'))
    print(tokenize('有兑换码吗？'))
    print(tokenize('有没有群'))
    print(tokenize('收到'))
    print(tokenize('有没有福利码'))
    print(tokenize('∨'))
    print(tokenize('礼包码是什么'))
    print(tokenize('送资源送功勋了 {localization:254-451}'))
    print(tokenize('40w {localization:519-473}'))
    print(tokenize('ziyuan18972079820'))
    print(tokenize('selling call V 19888310671'))
    print(tokenize('{scheduleMsg:1618741814-郑}'))
    print(tokenize('vip5个7'))
    print(tokenize('收的'))
    print(tokenize('群多少啊'))
    print(tokenize('怎么加'))
    print(tokenize('一百多万资源'))
    print(tokenize('小号去拉资源 {localization:482-837}'))
    print(tokenize('进攻了光源村:进攻了光源村'))
    print(tokenize('我加你'))
