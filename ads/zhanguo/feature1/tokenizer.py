# encoding: utf-8

import normalizer
import blocker
import subblocker
import recognizer
import remover

from typing import List, Union
from text import Text, Block, SubBlock

TextNormalized = str


def tokenzie(text: str) -> List[str]:

    def normalize(text: Text):
        text.normalized = normalizer.normalize(text.value)

    def blocking(text: Text):
        text.blocks = blocker.blocking(text.normalized)

    def recognize(text: Text):
        for block in text.blocks:
            _recognize_block(text, block)

    def _recognize_block(text: Text, block: Block):
        token = recognizer.recognize(block.value)
        if token:
            block.tokens = token
        else:
            subblocking(block)
            for subblock in block.subblocks:
                _recognize_subblock(text, subblock)

    def subblocking(block: Block):
        block.subblocks = subblocker.subblocking(block.value)

    def _recognize_subblock(text: Text, subblock: SubBlock):
        token = recognizer.recognize(subblock.value)
        if token:
            subblock.tokens = token
        else:
            return list[subblock.value]

    def remove(text: Text):
        text.mask = remover.remove(text.tokens)

    text = Text(text)
    normalize(text)
    blocking(text)
    recognize(text)
    remove(text)

    return text.tokens
