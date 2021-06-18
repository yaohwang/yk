# encoding: utf-8

import re
import time
import jieba
import opencc
cc = opencc.OpenCC('tw2s')


def convert(text: str) -> str:
    text = text.lower()
    text = cc.convert(text)
    return text


from typing import Union, List
from .tokenizer_base import normalize


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
    '[RES-S]',
    '[VIP]',
    '[WHO]',
    '[PLG]',
    '[OGM]',
    '[MNY]',
]

words_normal = [
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
    # '攻略',
    '交易猫',
    'good',
    'morning',
    'thanks',
    # 'go',
    # 'ha',
    '氪金',
    '黄金月卡',
    # '黄金',
    '谷歌',
    # '123',
    # '321',
    '如何',
    '欢迎',
    '孙膑',
    '大量',
    '秦国',
    '将令',
    '一起',
    'hello',
    'world',
    'me too',
    'welcome',
    'thank you',
    'night',
    '可以',
    '期待',
    '群雄',
    '方便',
    '沟通',
    '招募',
    '最新',
    '活动',
    '义渠乱军',
    '破解',
    '速度',
    '群英',
    '申请',
    'come on',
    'system',
    'yes sir',
    'xi tong',
    '依赖',
    'i love u',
    # 'respect',
    'sorry',
    'hi all',
    '麻烦',
    '尽快',
    '你好',
    '机会',
    '请问',
    '兴趣',
    '讨论',
    '出其不意',
    '疫情',
    '结束',
    '折扣',
    '需要',
    '新加坡',
    '诚心',
    '邀请',
    '日后',
    '沟通',
    '联络',
    '铁哥',
    'afternoon',
    'moring',
    '哈啰',
    'hihihi',
    '支援',
    '倒数',
    '武将',
    '橙装',
    '攻城',
    '谢谢',
    '公告',
    '防守',
    '提供',
    '争夺',
    '秦王',
    '威武',
    '你好',
    '私信',
    '马来西亚',
    '工作室',
    '燃烧队',
    '更多',
    '交流',
    '经验',
    '暂时',
    '停战',
    '休养生息',
    '等待',
    '下次',
    '天下大乱',
    'malaysia',
    '进团',
    '不懂',
    '铁木真',
    'lets go',
    'no problem',
    'ok thx',
    '明天',
    '热闹',
    '序号',
    '过来',
]

words_stop = ['了', '的', '啊', '吗', '吧', '呢', '~', '喔', '唷', '?', '？', '。', '哦', '呀', '谢谢', '请', '刚']
words_contact_method = ['微信号', '微信', '微', '扣扣', '群', '企鹅', '好友', '赖', 'qq', 'id']
words_resource = ['资源', '玉珏', '玉', '金', '木', '铁', '石', '书', '至尊卡', '黄金月卡']
words_resource_suspect = ['礼包码', '礼包', '兑换码', '福利码', '福利', '码', '攻略']
words_location = ['光源村', '白鹿村', '白阳村']

words_who_1 = ['你们', '我们', '他们', '老大', 
    # '团长',
    '新手', '活跃玩家', '大家', '各位', '高玩', '新老玩家', '大佬', '萌新', '自己']

words_who_2 = ['您', '你', '我', '他']

words_plugin = ['红手指', '春秋辅助']
words_game_other = ['鸿图', '三国志战略版', '龙狼']
words_money = ['钱', '马币', '台币', '港币']

words = []
words += words_normal
words += words_resource
words += words_resource_suspect
words += words_location
words += words_who_1
words += words_plugin
words += words_game_other
words += words_money

words_who = words_who_1 + words_who_2

words_2 = []
words_2 += words_who_2

words_all = words + words_2

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
        if '十' == text: return '加'

        text = _replace(text, 'ziyuan', '资源')

        text = _replace(text, '亻言', '信')

        text = _replace(
            text, 
            [
                '威',
                '徽',
                '徵',
                'vvv',
                '∨x',
                '∨',
                '؆',
                '薇',
                '嶶',
                '微新',
                '微信',
                '魏心',
                '巍信',
                'wechat',
            ], 
            '微'
        )

        text = _replace(text, ['十赖'], '加赖')
        text = _replace(text, ['十老大'], '加老大')

        text = _replace(
            text,
            [
                'lineid',
                'line',
                '濑',
                '懒',
            ],
            '赖'
        )

        text = _replace(
            text,
            [
                'qqid',
                'qqq',
            ],
            'qq'
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
                '添加一下',
                '加一下',
                '加下',
                '加入',
                '加啦',
                '咖',
                '架',
                '嫁',
                # '十',
                '茄',
                '迦',
                '联系',
                '笳',
                '十1',
                '加个',
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
                '初',
            ],
            '出'
        )

        text = _replace(
            text,
            [
                '仔媛',
                '籽援',
                '大米',
                '白菜',
            ],
            '资源'
        )

        text = _replace(
            text,
            [
                '课',
            ],
            '氪'
        )

        text = _replace(
            text,
            [
                'gogle',
                'google',
            ],
            '谷歌'
        )

        text = _replace(
            text,
            [
                '春秋m辅助',
            ],
            '春秋辅助'
        )

        text = _replace(
            text,
            [
                '私下',
                '私聊',
                '私讯',
                '信息',
            ],
            '私'
        )

        text = _replace(text, ['address'], '地址')

        text = _replace(
            text, 
            [
                '或者',
                '或是',
            ], 
            '或'
        )

        text = _replace(text, ['冇', '还有', '内有', '有人'], '有')

        text = _replace(
            text, 
            [
                'hahaha',
                'hahahaha',
                'hohoho',
                'yoyoyo',
            ],
            '哈'
        )

        text = _replace(text, ['障号', 'account'], '号')

        text = _replace(
            text,
            [
                'gogogo',
                'gogogogo',
                'go go go',
            ],
            '走'
        )

        text = _replace(
            text,
            [
                'zzzzzz',
            ],
            'z'
        )

        text = _replace(
            text,
            [
                '鸿图之下',
                '鸿图天下',
            ],
            '鸿图'
        )

        text = _replace(
            text,
            [
                'add oil',
            ],
            '加油'
        )

        text = _replace(text, ['什幺'], '什么')
        # text = _replace(text, ['私讯', '信息'], '私信')
        text = _replace(text, ['苔'], '台币')
        text = _replace(text, ['有木有'], '有没有')

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
    pattern_charnum = '[a-zA-Z%s_\s]+' % pattern_num

    pattern_location_token = '^\{localization:[%s]{1,3}\-[%s]{1,3}\}$' % (pattern_num, pattern_num)
    pattern_emoji_token = '^chatemoji:[%s]{1,2}$' % pattern_num
    pattern_charnum_token = '^[a-zA-Z%s_\s]+$' % pattern_num

    pattern_num1 = '[%s]+[多万]{1,}' % pattern_num
    pattern_num2 = '[%s]+个[%s]+' % (pattern_num, pattern_num)
    pattern_num3 = '[%s]+w' % pattern_num
    pattern_num0 = '[%s]+' % pattern_num

    pattern_num1_token = '^[%s]+[多万]{1,}$' % pattern_num
    pattern_num2_token = '^[%s]+个[%s]+$' % (pattern_num, pattern_num)
    pattern_num3_token = '^[%s]+w$' % pattern_num
    pattern_num0_token = '^[%s]+$' % pattern_num

    pattern_vip = 'vip'
    pattern_vip_token = '^vip$'

    pattern_tokens_1 = '(%s)' % '|'.join([
        pattern_location,
        pattern_emoji,
        pattern_charnum,
    ])

    def in_pattern_1(text: str) -> bool:
        return re.match(pattern_location_token, text) \
            or re.match(pattern_emoji_token, text) \
            or re.match(pattern_charnum_token, text)

    pattern_tokens_2 = '(%s)' % '|'.join([
        pattern_num1,
        pattern_num2,
        pattern_num3,
        pattern_num0,
        pattern_vip,
    ])

    pattern_words = '(%s)' % '|'.join(words)
    pattern_words_2 = '(%s)' % '|'.join(words_2)

    def coarse(text: str) -> List[str]:

        def _coarse(tokens: List[str], pattern) -> List[str]:
            new_tokens = []
            for token in tokens:
                if token in words_all or in_pattern_1(token):
                    new_tokens.append(token)
                else:
                    new_tokens.extend(valid_head_tail(re.split(pattern, token)))
            return new_tokens

        tokens = valid_head_tail(re.split(pattern_words, text))
        tokens = _coarse(tokens, pattern_words_2)
        tokens = _coarse(tokens, pattern_tokens_1)
        tokens = _coarse(tokens, pattern_tokens_2)
        return tokens
        

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
        # return is_location(token) \
        t = is_location(token) \
            or is_emoji(token) \
            or is_vip(token) \
            or token in words_normal
        return t

    def is_location(token: str) -> bool:
        return re.match(pattern_location_token, token) \
            or token in words_location

    def is_emoji(token: str) -> bool:
        return re.match(pattern_emoji_token, token)

    def is_vip(token: str) -> bool:
        return re.match(pattern_vip_token, token)

    def is_num(token: str) -> bool:
        return re.match(pattern_num1_token, token) \
            or re.match(pattern_num2_token, token) \
            or re.match(pattern_num3_token, token) \
            or re.match(pattern_num0_token, token)

    def is_charnum(token: str) -> bool:
        return re.match(pattern_charnum_token, token)

    def is_who(token: str) -> bool:
        return token in words_who

    def is_plugin(token: str) -> bool:
        return token in words_plugin

    def is_game_other(token: str) -> bool:
        return token in words_game_other

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
            elif text in ['v', 'vx', 'q', 'qq', 'id']: return ['[CTA-M]']
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
                # for word in words_resource:
                #     tokens = split(tokens, word)
                #     t = []
                #     for token in tokens:
                #         if is_special(token):
                #             t.append(token)
                #         elif token in words_resource:
                #             t.append('[RES]')
                #         else:
                #             t.append(token)
                #     tokens = t
                # return tokens

                tokens = ['[RES]' if token in words_resource else token for token in tokens]
                tokens = ['[RES-S]' if token in words_resource_suspect else token for token in tokens]
                return tokens

            def _recognize_plugin(tokens: List[str]) -> List[str]:
                return ['[PLG]' if token in words_plugin else token for token in tokens]

            def _recognize_game_other(tokens: List[str]) -> List[str]:
                return ['[OGM]' if token in words_game_other else token for token in tokens]

            def _recognize_money(tokens: List[str]) -> List[str]:
                return ['[MNY]' if token in words_money else token for token in tokens]

            tokens = [text]
            tokens = _recognize_contact_method(tokens)
            tokens = _recognize_resource(tokens)
            tokens = _recognize_plugin(tokens)
            tokens = _recognize_game_other(tokens)
            tokens = _recognize_money(tokens)
            return tokens

        # def _recognize_words(tokens: List[str]) -> List[str]:
        #     for word in words:
        #         tokens = split(tokens, word)
        #     return tokens

        if is_normal(text):
            tokens = _recognize_normal(text)
        elif is_num(text): 
            tokens = _recognize_num(text)
        elif is_charnum(text):
            tokens = _recognize_charnum(text)
        else:
            tokens = _recognize_other(text)
            tokens = flatten_once([_recognize_normal(token) for token in tokens])

        # tokens = _recognize_words(tokens)
        return tokens

    def stop_words(tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in words_stop]

    def to_single(tokens: List[str]) -> List[str]:
        return flatten_once([[token] if is_single(token) else list(token) for token in tokens])

    def remove_whitespace(tokens: List[str]) -> List[str]:
        tokens = [re.sub('\s', '', token) for token in tokens]
        tokens = [token for token in tokens if token]
        return tokens

    # normalize base
    text = text.lower()
    text = cc.convert(text)

    # normalize
    text = normalize(text)
    text = clean(text)
    text = extract(text)
    text = replace(text)

    # tokenize
    tokens = coarse(text)

    # recognize
    tokens = recognize(tokens)
    tokens = to_single(tokens)
    tokens = stop_words(tokens)
    tokens = remove_whitespace(tokens)

    return tokens


if __name__ == '__main__':
    # print(tokenize('0你好v123测试456%&-1'))
    # print(tokenize('微信号多少？'))
    # print(tokenize('微信多少'))
    # print(tokenize('108给3万玉要加扣扣730356479'))
    # print(tokenize('加油加油加油'))
    # print(tokenize('200多万资源'))
    # print(tokenize('资源爆满了'))
    # print(tokenize('chatemoji:7'))
    # print(tokenize('Theme:联盟邮件 Content: 进盟的兄弟都加下我微信gj203627，没加下线就当机器人踢了！！加我领礼包码攻略'))
    # print(tokenize('企鹅'))
    # print(tokenize('*收'))
    # print(tokenize('加团长徽：15183063671（梦瑶）我啦你们进群，领取对应的礼包码，不来的当机器人踢了'))
    print(tokenize('Theme:军团消息 Content: 兄弟我盟主，茄我徵NMML87，拉你进盟裙,方便统计活人分配职位，没来的下线当人机踢了'))
    # print(tokenize('有兑换码吗？'))
    # print(tokenize('有没有群'))
    # print(tokenize('收到'))
    # print(tokenize('有没有福利码'))
    # print(tokenize('∨'))
    # print(tokenize('礼包码是什么'))
    # print(tokenize('送资源送功勋了 {localization:254-451}'))
    # print(tokenize('40w {localization:519-473}'))
    # print(tokenize('ziyuan18972079820'))
    # print(tokenize('selling call V 19888310671'))
    # print(tokenize('{scheduleMsg:1618741814-郑}'))
    # print(tokenize('vip5个7'))
    # print(tokenize('收的'))
    # print(tokenize('群多少啊'))
    # print(tokenize('怎么加'))
    # print(tokenize('一百多万资源'))
    # print(tokenize('小号去拉资源 {localization:482-837}'))
    # print(tokenize('进攻了光源村:进攻了光源村'))
    # print(tokenize('我加你'))
    # print(tokenize('防守[刘邦算计]小老虎的進攻:防守*刘邦算计*小老虎的進攻'))
    # print(tokenize('有赖吗'))
    # print(tokenize('我的line是dgjunon'))
    # print(tokenize('加我yao_0713'))
    # print(tokenize('lineid：sheung_kwan1321aaqqid:634676841加我们军团群的人请走这边～一天没上线会踢')) # TODO:
    # print(tokenize('good morning'))
    # print(tokenize('gogogo'))
    # print(tokenize('就你没十老大嶶信了'))
    # print(tokenize('课金'))
    # print(tokenize('gogle搜寻春秋m辅助'))
    # print(tokenize('有要礼包的私下我'))
    # print(tokenize('address'))
    # print(tokenize('50新币/150马币=6玩玉钰6万黄金+line：6888k'))
    # print(tokenize('123123123'))
    # print(tokenize('stop_321'))
    # print(tokenize('line:kelvinchan8612'))
    # print(tokenize('z h e g u 9 0 8'))
    # print(tokenize('hi, 加入我们，一起玩吗'))
    # print(tokenize('theme:礼包码 content: 礼包码1heroccmm911eo888pin88888backccmmycbzq638769bqzze738975ccmtw0311'))
    # print(tokenize('你加我id'))
    # print(tokenize('你好呀，请问有机会加入我们吗'))
    # print(tokenize('我想加入你们'))
    # print(tokenize('911eo888'))
    # print(tokenize('hi 你也是刚玩的吗'))
    # print(tokenize('三国志战略版'))
