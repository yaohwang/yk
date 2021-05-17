# encoding: utf-8

from typing import List, Union, Tuple, Optional
from .unicode_mapping import is_enclosed_alphanumerics
from .unicode_mapping import is_small_form_variants
from .unicode_mapping import is_halfwidth_and_fullwidth_forms

Char = str


def normalize(text: str) -> str:
    return ''.join(_normalize(c) for c in text)


def _normalize(c: Char) -> Char:

    def enclosed_alphanumerics_to_basic_latin(c: Char) -> Char:

        def numeric(code: int) -> int:
            code = zero(code)
            if isinstance(code,int) and code == code: code = one_to_nine(code)
            if isinstance(code,int) and code == code: code = ten_to_nineteen(code)
            if isinstance(code,int) and code == code: code = twenty(code)
            return code

        def zero(code: int) -> int:
            return 0x0030 if 0x24ea == code \
                or 0x24ff == code \
                else code

        def one_to_nine(code: int) -> int:
            if 0x2460 <= code and 0x2468 >= code:
                return code-0x242f 
            elif 0x2474 <= code and 0x247c >= code:
                return code-0x2443
            elif 0x2488 <= code and 0x2490 >= code:
                return code-0x2457
            elif 0x24f5 <= code and 0x24fd >= code:
                return code-0x24c4
            return code

        def ten_to_nineteen(code: int) -> int:
            if 0x2469 <= code and 0x2472 >= code:
                return [0x0031, code-0x2439]
            elif 0x247d <= code and 0x2486 >= code:
                return [0x0031, code-0x244d]
            elif 0x2491 <= code and 0x249a >= code:
                return [0x0031, code-0x2461]
            elif 0x24eb <= code and 0x24f3 >= code: # 11-19
                return [0x0031, code-0x24ba]
            elif 0x24fe == code: # 10
                return [0x0031, 0x0030]
            return code

        def twenty(code: int) -> int:
            return [0x0032, 0x0030] if 0x2473 == code \
                or 0x2487 == code \
                or 0x249b == code \
                or 0x24f4 == code \
                else code

        def alphabet(code: int) -> int:
            code = alphabet_lower(code)
            if isinstance(code,int) and code == code: code = alphabet_upper(code)
            return code

        def alphabet_lower(code: int) -> int:
            if 0x249c <= code and 0x24b5 >= code:
                return code-0x243b
            elif 0x24d0 <= code and 0x24e9 >= code:
                return code-0x246f
            return code

        def alphabet_upper(code: int) -> int:
            if 0x24b6 <= code and 0x24cf >= code:
                return code-0x2475
            return code

        code = ord(c)
        code = numeric(code)
        if isinstance(code,int) and code == code: code = alphabet(code)
        if isinstance(code, int):
            return chr(code)
        elif isinstance(code, list):
            return ''.join([chr(c) for c in code])
        else:
            raise ValueError(
                f"type of code unknown: {type(code)}. "
                f"Should be one of a str or list."
            )  

    def small_form_variants_to_basic_latin(c: Char) -> Char:
        mapping = {
            0xfe50 : 0x002c,
            0xfe51 : 0x3001, # CJK Symbols and Punctuation
            0xfe52 : 0x002e,

            0xfe54 : 0x003b,
            0xfe55 : 0x003a,
            0xfe56 : 0x003f,
            0xfe57 : 0x0021,
            0xfe58 : 0x2014, # General Punctuation
            0xfe59 : 0x0028,
            0xfe5a : 0x0029,
            0xfe5b : 0x007b,
            0xfe5c : 0x007d,
            0xfe5d : 0x005b,
            0xfe5e : 0x005d,
            0xfe5f : 0x0023,
            0xfe60 : 0x0026,
            0xfe61 : 0x002a,
            0xfe62 : 0x002b,
            0xfe63 : 0x002d,
            0xfe64 : 0x003c,
            0xfe65 : 0x003e,
            0xfe66 : 0x003d,

            0xfe68 : 0x005c,
            0xfe69 : 0x0024,
            0xfe6a : 0x0025,
            0xfe6b : 0x0040,
        }
        code = mapping.get(ord(c))
        return chr(code) if code else c

    def halfwidth_and_fullwidth_forms_to_basic_latin(c: Char) -> Char:
        code = ord(c)
        if 0xff01 <= code and 0xff5e >= code:
            return chr(code-0xfee0)
        return c

    if is_enclosed_alphanumerics(c):
        return enclosed_alphanumerics_to_basic_latin(c)
    elif is_small_form_variants(c):
        return small_form_variants_to_basic_latin(c)
    elif is_halfwidth_and_fullwidth_forms(c):
        return halfwidth_and_fullwidth_forms_to_basic_latin(c)
    return c
