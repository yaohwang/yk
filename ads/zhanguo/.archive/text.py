# encoding: utf-8

from collections import namedtuple
from itertools import compress
from typing import Dict, List, Tuple, Any, Union

Char = str
Slice = namedtuple('Slice', ['start', 'end'])
SliceValue = namedtuple('SliceValue', ['slice', 'value'])

class TextNormalized: pass
class Block: pass
class SubBlock: pass
class Token: pass


class Text(object):

    def __init__(self, text: str):
        self.value: List[str] = list(text)
        self._normalized: TextNormalized = None
        self._blocks: List[Block] = []
        self._mask: List[int] = []

    @property
    def normalized(self):
        return self._normalized

    @normalized.setter
    def normalized(
        self, 
        obj: Union[TextNormalized, List[SliceValue], List[Tuple[Tuple[int,int],str]]]
    ):
        if isinstance(obj, list):
            e0 = obj[0]
            if isinstance(e0, SliceValue):
                self._normalized = TextNormalized(self, obj)
            elif isinstance(e0, tuple):
                obj = [SliceValue(Slice(start,end),s) for ((start,end),s) in obj]
                self._normalized = TextNormalized(self, obj)
            else:
                raise ValueError(
                    f"type of obj unknown: {type(obj[i])}. "
                    f"Should be one of a SliceValue, Tuple."
                )  
        elif isinstance(obj, TextNormalized):
            obj.parent = self
            self._normalized = obj
        else:
            raise ValueError(
                f"type of obj unknown: {type(obj)}. "
                f"Should be one of a list, TextNormalized."
            )  

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(
        self,
        obj: List[Union[Block, Slice, Tuple]]
    ):
        if isinstance(obj, list):
            e0 = obj[0]
            if isinstance(e0, Block):
                for _ in obj: _.parent = self.normalized
                self._blocks = obj
            elif isinstance(e0, Slice):
                self._blocks = [Block(self.normalized,slc) for slc in obj]
            elif isinstance(e0, Tuple):
                self._blocks = [Block(self.normalized,Slice(*tpl)) for tpl in obj]
            else:
                raise ValueError(
                    f"type of obj unknown: {type(obj[i])}. "
                    f"Should be one of a Block, Slice, Tuple."
                )  
        else:
            raise ValueError(
                f"type of obj unknown: {type(obj)}. "
                f"Should be a list."
            )  

    @property
    def tokens(self):
        _tokens = [token for block in self.blocks for token in block.tokens]
        if self.mask: _tokens = compress(_tokens, self.mask)
        return _tokens

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, obj: List[int]):
        self._mask = obj


class TextNormalized(object):

    def __init__(self, parent: Text, mapping: List[SliceValue]):
        self.parent = parent
        self.mapping = sorted(mapping)
        self._tokens = []

    @property
    def value(self):
        return slice_replace(self.parent.value, self.mapping)


class BaseBlock(object):

    def __init__(self, parent: Any, slc: Slice):
        self.parent = parent
        self.slc = slc

    @property
    def value(self):
        self.parent.value[self.slc]

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, obj: Union[List[Token], List[str], Token, str]) -> List[Token]:
        if isinstance(obj, list):
            e0 = obj[0]
            if isinstance(e0, Token):
                for _ in obj: _.parent = self
                self._tokens = obj
            elif isinstance(e0, str):
                self._tokens = [Token(self,_) for _ in obj]
            else:
                raise ValueError(
                    f"type of obj unknown: {type(obj[i])}. "
                    f"Should be one of a Block, Slice, Tuple."
                )  
        elif isinstance(obj, Token):
            obj.parent = self
            self._tokens = [obj]
        elif isinstance(obj, str):
            self._tokens = [Token(self, obj)]
        else:
            raise ValueError(
                f"type of obj unknown: {type(obj)}. "
                f"Should be one of a list, TextNormalized."
            )  
    

class Block(BaseBlock):

    def __init__(self, parent: TextNormalized, slc: Slice):
        super(Block, self).__init__(parent, slc)
        self._subblocks = []

    @property
    def subblocks(self):
        return self._subblocks

    @subblocks.setter
    def subblocks(
        self,
        obj: List[Union[SubBlock, Slice, Tuple]]
    ):
        if isinstance(obj, list):
            e0 = obj[0]
            if isinstance(e0, SubBlock):
                for _ in obj: _.parent = self
                self._subblocks = obj
            elif isinstance(e0, Slice):
                self._subblocks = [SubBlock(self,slc) for slc in obj]
            elif isinstance(e0, Tuple):
                self._subblocks = [SubBlock(self,Slice(*tpl)) for tpl in obj]
            else:
                raise ValueError(
                    f"type of obj unknown: {type(obj[i])}. "
                    f"Should be one of a SubBlock, Slice, Tuple."
                )  
        else:
            raise ValueError(
                f"type of obj unknown: {type(obj)}. "
                f"Should be a list."
            )  

    @property
    def tokens(self):
        return self._tokens if not self.subblocks else [
            token for subblock in self.subblocks for token in subblock.tokens
        ]
        


class SubBlock(BaseBlock):

    pass


class Token(object):

    def __init__(self, parent: Union[Block, SubBlock], value: str):
        self.parent = parent
        self.value = value

    @property
    def slicevalue(self):
        if isinstance(self.parent, Block):
            return SliceValue(self.parent.slice, value)
        elif isinstance(self.parent, SubBlock):
            slc_base = self.parent.parent.slice.start
            slc_start = slc_base + self.parent.slice.start
            slc_end = slc_base + self.parent.slice.end
            return SliceValue(Slice(slc_start, slc_end), value)
        else:
            raise ValueError(
                f"type of self.parent unknown: {type(self.parent)}. "
                f"Should be one of a Block or SubBlock."
            )  
        


def slice_replace(text: List[str], mapping: List[SliceValue]) -> List[str]:
	# TODO: test
    # len(mapping) = 0
    if not mapping: return text
    r = []
    r.extend(text.value[:mapping[0].slice.start])
    # len(mapping) >= 2
    if 2 <= len(mapping):
        for i in range(len(mapping)-1):
            r.append(mapping[i].value)
            r.extend(text.value[mapping[i].slice.end:mapping[i+1].slice.start])
    # len(mapping) = 1 or len(mapping) >= 2 last
    r.append(mapping[-1].value)
    r.extend(text.value[mapping[-1].slice.end:])
    # keep valid only
    r = [_ for _ in r if _]
    return r


if __name__ == '__main__':
    text = Text('0123456789')
    mapping = [
        SliceValue(Slice(0, 2), 'a'),
        SliceValue(Slice(2, 3), 'b'),
        SliceValue(Slice(4, 6), 'c'),
        SliceValue(Slice(9, 10), 'd'),
    ]
    print(slice_replace(text, mapping))
