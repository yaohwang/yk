# encoing: utf-8

pattern_num = '0-9零一二三四五六七八九十百千万亿'
pattern_location = '\{localization:[%s]{1,3}\-[%s]{1,3}\}' % (pattern_num, pattern_num)
pattern_emoji = 'chatemoji:[%s]{1,2}' % pattern_num
pattern_num1 = '[%s]+[多万]{1,}' % pattern_num
pattern_num2 = '[%s]+个[%s]+' % (pattern_num, pattern_num)
pattern_num3 = '[%s]+w' % pattern_num
pattern_num0 = '[%s]+' % pattern_num
pattern_vip = 'vip'
pattern_charnum = '[a-zA-Z%s_]+' % pattern_num

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

def blocking(text: str) -> List[Tuple[int,int]]:
    return valid_head_tail(re.split(pattern_tokens, text))
