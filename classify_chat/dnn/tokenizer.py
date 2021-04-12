# encoding: utf-8

import os
import re
import jieba
import hanlp

from itertools import chain
from itertools import zip_longest
from mih import Step
from mih import Pipeline
from mih import NormalizerBase
from mih import VocabularyBase as Vocabulary
from typing import List, Set, Dict, Union, Tuple, Optional, Any, Callable
from transformers.models.bert.tokenization_bert import BertTokenizer


# Define type aliases
Char = str 
CharsInput = List[Char]
CharsOutput = CharsInput

Token = Char
TokenId = int 
TokenInput = List[Token]
TokenOutput = TokenInput

Text = str 
TextInput = List[Text]
TextFrom = Text
TextTo = Text

Name = str 
Required = List[Name]
Function = Callable[[Any],Any]
Args = List
Kwargs = Dict
FunctionTuple = Union[
    Tuple[Function],
    Tuple[Function, Args],
    Tuple[Function, Kwargs],
    Tuple[Function, Args, Kwargs],
    Tuple[Function, Args, Required],
    Tuple[Function, Kwargs, Required],
    Tuple[Function, Args, Kwargs, Required],
]

# Define global
HanLP = hanlp.load(hanlp.pretrained.mtl.UD_ONTONOTES_TOK_POS_LEM_FEA_NER_SRL_DEP_SDP_CON_XLMR_BASE)

class FlattenList(list):

    def flatten_append(self, e: Union[str, List[str]]):
        if isinstance(e, str):
            self.append(e)
        elif isinstance(e, list):
            self.extend(e)
        else:
            raise ValueError(
                f"type of e unknown: {type(e)}. "
                f"Should be one of a str or list[str]."
            ) 


class NormalizerSGZChat(Pipeline):

    def __init__(
        self,
        callables: List[Union[Name, Step, FunctionTuple]]=[
            'normalize_unicode_char',
            str.lower,
            lambda s: str.replace(s, '*', ''),
            'drop_redundancy',
            'retrieve',
            'extract_special_tokens',
            'drop_nonsense',
            'to_list',
            # 'split_jieba',
            # 'split_hanlp',
        ],
        **kwargs
    ):
        super().__init__(callables, **kwargs)
        self.normalizer_base = NormalizerBase()
        self.special_tokens = ['[UNK]', '[LOC]', '[BTL]', '[URL]', '[VIP]', '[SYS]', '[NUM-REP]', '[CTA]', '[NUM]', '[EMJ]']

    def _flatten(self, l: Union[str, List[Union[str, List]]]) -> List[str]:
        if isinstance(l, str): return l
        r = []
        for e in l:
            if isinstance(e, str):
                r.append(e)
            else:
                r.extend(e)
        return r

    def _step(
        self,
        s: Union[str, List[str]],
        func: Callable[[str], Union[str, List[str]]],
        *args,
        **kwargs
    ) -> Union[str, List[str]]:
        if isinstance(s, str):
            return self._flatten(func(s, *args, **kwargs))
        elif isinstance(s, list):
            return self._flatten([func(_, *args, **kwargs) for _ in s])
        else:
            raise ValueError(
                f"type of s unknown: {type(s)}. "
                f"Should be one of a str or list[str]."
            ) 

    def normalize_unicode_char(self, s: str) -> str:
        return ''.join([self.normalizer_base(c) for c in s])

    def drop_redundancy(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def drop_repeats(s: Union[str, List[str]], codes: List[int]):
            return self._step(s, _drop_repeats, codes)

        def _drop_repeats(s: str, codes: List[int]):
            if s in self.special_tokens: return s
            for code in codes:
                char = chr(code)
                try:
                    if 0x002e == code or 0x003f == code:
                        s = re.sub('\%s{2,}' % char, char, s)
                    else:
                        s = re.sub('%s{2,}' % char, char, s)
                    # s = re.sub('\\u%04x{2,}' % code, char, s)
                except:
                    pass
            return s

        def drop_repeats_symbol(s: Union[str, List[str]]):
            symbols = []
            symbols.extend(range(0x0021, 0x002e+1)) # no 0x002f /, for url recognize need.
            symbols.extend(range(0x003a, 0x0040+1))
            symbols.extend(range(0x005b, 0x0060+1))
            symbols.extend(range(0x007b, 0x007e+1))
            symbols.extend(range(0x0080, 0x00ff+1))
            symbols.extend(range(0x2000, 0x206f+1))
            symbols.extend(range(0x3000, 0x303f+1))

            return drop_repeats(
                s,
                symbols
            )

        s = drop_repeats_symbol(s)
        return s

    def retrieve(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def retrieve_info(s: Union[str, List[str]], mapping: List[Tuple[TextFrom,TextTo]]):
            return self._step(s, _retrieve_info, mapping)

        def _retrieve_info(s: str, mapping: List[Tuple[TextFrom,TextTo]]):
            if s in self.special_tokens: return s
            for (f, t) in mapping:
                s = s.replace(f, t)
            return s

        def retrieve_from_symbol(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    # ('十', '加'),
                    (u'\u2191', '上'), # ↑ -> 上
                    (u'\u2193', '下'), # ↓ -> 下
                ]
            )

        def retrieve_from_pinyin(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    ('威', '微'),
                    ('架', '加'),
                    ('嫁', '加'),
                    ('冲', '充'),
                    ('础', '出'),
                    ('麦', '卖'),
                    ('huodong', '活动'),
                    ('waigua', '外挂'),
                ]
            )

        def retrieve_from_shape(s: Union[str, List[str]]):
            
            def retrieve_from_shape_single(s: Union[str, List[str]]):
                return retrieve_info(
                    s, 
                    mapping=[
                        ('徽', '微'),
                        ('徵', '微'),
                        ('咖', '加'),
                        ('茄', '加'),
                        ('迦', '加'),
                        ('圕', '团'),
                    ]
                )

            def retrieve_from_shape_multi(s: Union[str, List[str]]):
                return retrieve_info(
                    s, 
                    mapping=[
                        ('亻言', '信'),
                        ('微新', '微信'),
                    ]
                )

            s = retrieve_from_shape_single(s)
            s = retrieve_from_shape_multi(s)
            return s

        def retrieve_to_abc(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    (u'\u2179', u'\u00d7'), # ⅹ -> ×
                    (u'\u2169', u'\u00d7'), # Ⅹ -> ×
                    (u'\u02e2', 's'), # ˢ -> s
                    (u'\u042c', 'b'), # Ь -> b
                    (u'\u1d52', 'o'), # ᵒ -> o
                    (u'\u1d4f', 'k'), # ᵏ -> k
                    (u'\u1d47', 'b'), # ᵇ -> b
                    (u'\u2164', 'v'), # Ⅴ -> v
                    (u'\u2174', 'v'), # ⅴ -> v
                    (u'\u2170', 'i'), # ⅰ -> i
                    (u'\u221a', 'v'), # √ -> v
                    (u'\u2228', 'v'), # ∨ -> v
                ]
            )

        def retrieve_to_num(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    (u'\u041e', '0'), # О -> 0
                    (u'\u2076', '6'), # ⁶ -> 6
                    (u'\u2171', '2'), # ⅱ -> 2
                    (u'\u2161', '2'), # Ⅱ -> 2
                    (u'\u3061', '5'), # ち -> 5
                ]
            )

        def retrieve_to_abc_num(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    (u'\u2165', 'v1'), # Ⅵ -> v1
                ]
            )

        def retrieve_to_symbol(s: Union[str, List[str]]):
            return retrieve_info(
                s, 
                mapping=[
                    (u'\u22ef', u'\u2026'), # ⋯ -> …
                ]
            )

        s = retrieve_from_symbol(s)
        s = retrieve_from_pinyin(s)
        s = retrieve_from_shape(s)
        s = retrieve_to_abc(s)
        s = retrieve_to_num(s)
        s = retrieve_to_abc_num(s)
        return s

    def extract_special_tokens(self, s: str) -> List[str]:

        def extract_special(
            s: Union[str, List[str]],
            reg: str,
            special_token: Union[str, List[str]],
            reg_not: str=None
        ):
            return self._step(s, _extract_special, reg, special_token)

        def _extract_special(
            s: str,
            reg: str,
            special_token: Union[str, List[str]]
        ):
            if s in self.special_tokens: return s
            r = re.split(reg, s)
            if 1 >= len(r): return r
            # r = list(chain.from_iterable(zip_longest(r[:-1], [], fillvalue=special_token))) + r[-1:]
            # return [i for i in r if i]
            result = FlattenList()
            for i in range(len(r)-1):
                if '' == r[i]:
                    result.flatten_append(special_token)
                else:
                    result.flatten_append(r[i])
                    if '' != r[i+1]:
                        result.flatten_append(special_token)
            if not (2==len(r) and ''==r[0] and ''==r[1]):
                result.flatten_append(special_token if '' == r[-1] else r[-1])
            return result

        def extract_pattern(
            s: Union[str, List[str]],
            reg: str,
            reg_not: str,
            special_token: Union[str, List[str]]
        ):
            return self._step(s, _extract_pattern, reg, reg_not, special_token)

        def _extract_pattern(
            s: str,
            reg: str,
            reg_not: str,
            special_token: Union[str, List[str]]
        ):
            if s in self.special_tokens: return s
            i = 0
            not_match = []
            result = FlattenList()
            while(i < len(s)):
                r1 = re.match(reg, s[i:])
                r2 = re.match(reg_not, s[i:])
                if r1 and ((not r2) or (r2 and r1.group()==r2.group())):
                    if not_match:
                        result.append(''.join(not_match))
                        not_match = []
                    result.append(special_token)
                    i += len(r1.group())
                else:
                    not_match.append(s[i])
                    i += 1
            if not_match:
                result.append(''.join(not_match))
            return result

        def extract_loc(s: Union[str, List[str]]):
            return extract_special(s, r'{localization:[0-9]+\-[0-9]+}', '[LOC]')

        def extract_battle(s: Union[str, List[str]]):
            return extract_special(s, r'^{battle:[0-9]+,【.*】.*}$', '[BTL]')

        def extract_url(s: Union[str, List[str]]):
            return extract_special(s, r'[{]?[a-z]*[:]?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[}]?', '[URL]')
            # return extract_special(s, r'[\{]?[a-z]*[:]?http[s]?://[a-z0-9\./\-=$_@&\+!\*\(\),:]+[\}]?', '[URL]')

        def extract_sys(s: Union[str, List[str]]):
            # TODO:
            return s

        def extract_vip(s: Union[str, List[str]]):
            return extract_pattern(s, r'(v[i]?[p]?[0-9]{1,2})|(vip)', r'v[i]?[p]?[0-9]{3,}', '[VIP]')

        def extract_money(s: Union[str, List[str]]):
            return extract_special(s, r'[0-9]+w', ['[NUM]', '万'])

        def extract_num_repeat(s: Union[str, List[str]]):
            return extract_special(s, r'0{5,}|1{5,}|2{5,}|3{5,}|4{5,}|5{5,}|6{5,}|7{5,}|8{5,}|9{5,}', '[NUM-REP]')

        def extract_contact(s: Union[str, List[str]]):

            def extract_abc_num(s: Union[str, List[str]]):
                # length >= 5
                # return extract_special(s, r'[0-9a-z]{5,}', '[CTA]')
                s = extract_special(s, r'[a-z]+[0-9]+[a-z0-9]+', '[CTA]')
                s = extract_special(s, r'[0-9]+[a-z]+[a-z0-9]+', '[CTA]')
                return s

            def extract_num(s: Union[str, List[str]]):
                # length >= 8
                # TODO: changeable
                return extract_special(s, r'[0-9]{8,}', '[CTA]')

            s = extract_abc_num(s)
            s = extract_num(s)
            return s

        def extract_num_normal(s: Union[str, List[str]]):
            return extract_special(s, r'[0-9]+', '[NUM]')

        def extract_emoji(s: Union[str, List[str]]):
            """
            - Basic Latin
            - Latin-1 Supplement
            - General Punctuation
            - CJK Symbols and Punctuation
            - CJK Unified Ideographs Extension A
            - CJK Unified Ideographs
            """
            # length >= 3
            return extract_special(s, u'[^\u0030-\u0039\u0041-\u005a\u0061-\u007a\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff]{3,}', '[EMJ]')

        s = extract_loc(s)
        s = extract_battle(s)
        s = extract_url(s)
        s = extract_sys(s)
        s = extract_vip(s)
        s = extract_money(s)
        s = extract_num_repeat(s)
        s = extract_contact(s)
        s = extract_num_normal(s)
        s = extract_emoji(s)
        return s

    def drop_nonsense(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def drop(s: Union[str, List[str]], reg: str):
            return self._step(s, _drop, reg)

        def _drop(s: str, reg: str):
            if s in self.special_tokens: return s
            return re.sub(reg, '', s)

        def drop_nonvalid_char(s: Union[str, List[str]]):
            return drop(s, u'[^\u0000-\u007f\u0080-\u00ff\u2000-\u206f\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff]+')

        def drop_punctuation(s: Union[str, List[str]]):
            return drop(s, u'[^\u0061-\u0071\u0030-\u0039\u3400-\u4dbf\u4e00-\u9fff]+')

        s = drop_nonvalid_char(s)
        s = drop_punctuation(s)
        return s

    def to_list(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def str_to_list(s: Union[str, List[str]]):
            return self._step(s, _str_to_list)

        def _str_to_list(s: str):
            if s in self.special_tokens: return s
            if 1 == len(s): return s
            return list(s)

        return str_to_list(s)

    def split_jieba(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def split(s: Union[str, List[str]]):
            return self._step(s, _split)

        def _split(s: str):
            if s in self.special_tokens: return s
            return jieba.lcut(s)
            
        s = split(s)
        return s

    def split_hanlp(self, s: Union[str, List[str]]) -> Union[str, List[str]]:

        def split(s: Union[str, List[str]]):
            return self._step(s, _split)

        def _split(s: str):
            if s in self.special_tokens: return s
            return HanLP(s)['tok']
            
        s = split(s)
        return s


class VocabularySGZChat:

    def create_vocab(self, texts_or_path: Union[TextInput, os.PathLike], **kwargs):
        # TODO: choose vocabulary class by kwargs
        # TODO: lazy init
        raise NotImplementedError


class TokenizerSGZChat(BertTokenizer):

    # def __init__(self, vocab: Vocabulary=None, **kwargs):
        # TODO:
        # raise NotImplementedError

    def _tokenize(self, text: Text, **kwargs) -> TokenOutput:
        return NormalizerSGZChat()(text)
