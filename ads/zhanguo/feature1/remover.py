# encoding: utf-8

def remove(tokens: List[str]) -> List[int]:

    def stop_words(tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in words_stop]

    def to_single(tokens: List[str]) -> List[str]:
        return flatten_once([[token] if is_single(token) else list(token) for token in tokens])

    def remove_whitespace(tokens: List[str]) -> List[str]:
        tokens = [re.sub('\s', '', token) for token in tokens]
        tokens = [token for token in tokens if token]
        return tokens

    # TODO:
