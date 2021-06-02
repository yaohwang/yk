# encoding: utf-8

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

            tokens = [text]
            tokens = _recognize_contact_method(tokens)
            tokens = _recognize_resource(tokens)
            return tokens

        def _recognize_words(tokens: List[str]) -> List[str]:
            for word in words:
                tokens = split(tokens, word)
            return tokens

        if is_normal(text):
            tokens = _recognize_normal(text)
        elif is_num(text):
            tokens = _recognize_num(text)
        elif is_charnum(text):
            tokens = _recognize_charnum(text)
        else:
            tokens = _recognize_other(text)
            tokens = flatten_once([_recognize_normal(token) for token in tokens])

        print(tokens)

        tokens = _recognize_words(tokens)
        return tokens
