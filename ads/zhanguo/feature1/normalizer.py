# encoding: utf-8

import opencc
import tokenizer_base

cc = opencc.OpenCC('tw2s')


def normalize(text: str) -> List[Tuple[Tuple[int,int],str]]:

    pattern_email = 'theme:(.*)content:(.*)'
    pattern_schedulemsg = '\{schedulemsg:[0-9]{10}-(.*)\}'

    def extract(text: str) -> str, List[Tuple[Tuple[int,int],str]]:
        slicevalue = []
        r = re.match(pattern_email, text)
        if r: 
            text = ''.join(r.groups())
            slicevalue = [((0,6),''), ((r.regs[1][1],r.regs[2][0]),'')]
            return text, slicevalue
        r = re.match(pattern_schedulemsg, text)
        if r:
            text = ''.join(r.groups())
            slicevalue = [((0,r.regs[1][0]),''), ((r.regs[1][1],r.endpos),'')]
            return text, slicevalue
        return text, slicevalue

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
                '薇',
            ],
            '微'
        )

        text = _replace(
            text,
            [
                'lineid',
                'line',
                '濑',
            ],
            '赖'
        )

        text = _replace(
            text,
            [
                'qqid',
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
                '加一下',
                '加下',
                '加入',
                '咖',
                '架',
                '嫁',
                '十',
                '茄',
                '迦',
                '联系',
                '笳',
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

    text = text.lower()
    text = cc.convert(text)
    text = tokenizer_base.normalize(text)

    text, slicevalue = extract(text)
    text = clean(text)

    text = replace(text)

    return text
