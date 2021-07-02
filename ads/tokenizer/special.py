# encoding: utf-8

from collections import namedtuple

""" special
"""

Special = namedtuple('Special', [
    'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6', 'NUM7',
    'LOC',
    'EMJ',
    'ABU',
    'CTAM', 'CTA',
    'ADD',
    'TRS', 'TRS3RD',
    'RES', 'RESS',
    'VIP',
    'WHO',
    'PLG',
    'OGM',
    'MNY',
    'URL',
    'AUD',
    'HAO',
],
defaults=[
    '[NUM]-1', '[NUM]-2', '[NUM]-3', '[NUM]-4', '[NUM]-5', '[NUM]-6', '[NUM]-7',
    '[LOC]',
    '[EMJ]',
    '[ABU]',
    '[CTA-M]', '[CTA]',
    '[ADD]',
    '[TRS]', '[TRS-3RD]',
    '[RES]', '[RES-S]',
    '[VIP]',
    '[WHO]',
    '[PLG]',
    '[OGM]',
    '[MNY]',
    '[URL]',
    '[AUD]',
    '[HAO]',
])

special = Special()


""" special num
"""

SpecialNum = namedtuple('SpecialNum', [
    'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6', 'NUM7',
],
defaults=[
	special.NUM1, special.NUM2, special.NUM3, special.NUM4, special.NUM5, special.NUM6, special.NUM7,
])

specialnum = SpecialNum()


""" special 0
"""

Special0 = namedtuple('Special0', [
	'EMJ', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6', 'NUM7', 'ABU', 'WHO', 'AUD',
],
defaults=[
	special.EMJ, special.NUM1, special.NUM2, special.NUM3, special.NUM4, special.NUM5, special.NUM6, special.NUM7, special.ABU, special.WHO, special.AUD,
])

special0 = Special0()


""" special 1
"""

Special1 = namedtuple('Special1', [
	'OGM', 'TRS3RD',
],
defaults=[
	special.OGM, special.TRS3RD,
])

special1 = Special1()


""" special 2
"""

Special2 = namedtuple('Special2', [
	'LOC', 'CTAM', 'CTA', 'TRS', 'RES', 'RESS', 'VIP', 'PLG', 'MNY', 'URL', 'ADD', 'HAO',
],
defaults=[
	special.LOC, special.CTAM, special.CTA, special.TRS, special.RES, special.RESS, special.VIP, special.PLG, special.MNY, special.URL, special.ADD, special.HAO,
])

special2 = Special2()


def pprint(nt):
	for k, v in nt._asdict().items():
	    print(k, v)
	print()


if __name__ == '__main__':
	pprint(special)
	pprint(specialnum)
	pprint(special0)
	pprint(special1)
	pprint(special2)
