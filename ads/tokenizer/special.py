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
    'AGR',
    'TRS', 'TRS3RD', 'TRSBHV', 'TRSSUS',
    'RES', 'RESS',
    'VIP',
    'WHO',
    'PLG',
    'OGM',
    'MNY',
    'URL',
    'AUD',
    'HAO',
    'SYS',
    'SALE',
    'TSP',
    'NEED',
    'HVN',
    'FIT',
],
defaults=[
    '[NUM]-1', '[NUM]-2', '[NUM]-3', '[NUM]-4', '[NUM]-5', '[NUM]-6', '[NUM]-7',
    '[LOC]',
    '[EMJ]',
    '[ABU]',
    '[CTA-M]', '[CTA]',
    '[ADD]',
    '[AGR]',
    '[TRS]', '[TRS-3RD]', '[TRS-BHV]', '[TRS-SUS]',
    '[RES]', '[RES-S]',
    '[VIP]',
    '[WHO]',
    '[PLG]',
    '[OGM]',
    '[MNY]',
    '[URL]',
    '[AUD]',
    '[HAO]',
    '[SYS]',
    '[SALE]',
    '[TSP]',
    '[NEED]',
    '[HVN]',
    '[FIT]',
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
	'EMJ', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6', 'NUM7', 'ABU', 'WHO', 'AUD', 'HVN', 'FIT',
],
defaults=[
	special.EMJ, special.NUM1, special.NUM2, special.NUM3, special.NUM4, special.NUM5, special.NUM6, special.NUM7, special.ABU, special.WHO, special.AUD, special.HVN, special.FIT,
])

special0 = Special0()


""" special 1
"""

Special1 = namedtuple('Special1', [
	'OGM', 'TRS3RD', 'TSP',
],
defaults=[
	special.OGM, special.TRS3RD, special.TSP,
])

special1 = Special1()


""" special 2
"""

Special2 = namedtuple('Special2', [
	'LOC', 'CTAM', 'CTA', 'TRS', 'TRSBHV', 'TRSSUS', 'RES', 'RESS', 'VIP', 'PLG', 'MNY', 'URL', 'ADD', 'AGR', 'HAO', 'SALE', 'NEED',
],
defaults=[
	special.LOC, special.CTAM, special.CTA, special.TRS, special.TRSBHV, special.TRSSUS, special.RES, special.RESS, special.VIP, special.PLG, special.MNY, special.URL, special.ADD, special.AGR, special.HAO, special.SALE, special.NEED,
])

special2 = Special2()


""" special risk
"""

SpecialRisk = namedtuple('SpecialRisk', [
	'OGM', 'TRS3RD', 'TSP', 'TRS', 'TRSBHV', 'TRSSUS', 'RES', 'VIP', 'PLG', 'MNY', 'URL', 'HAO', 'SALE',
],
defaults=[
	special.OGM, special.TRS3RD, special.TSP, special.TRS, special.TRSBHV, special.TRSSUS, special.RES, special.VIP, special.PLG, special.MNY, special.URL, special.HAO, special.SALE,
])

specialrisk = SpecialRisk()


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
