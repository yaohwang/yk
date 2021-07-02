# encoding: utf-8

from .fmm import tokenize

if __name__ == '__main__':
    print(' preprocess '.center(50, '-'))
    tokenize('Theme:联盟邮件 Content: 进盟的兄弟都加下我微信gj203627，没加下线就当机器人踢了！！加我领礼包码攻略')
    tokenize('Theme:军团消息 Content: 兄弟我盟主，茄我徵NMML87，拉你进盟裙,方便统计活人分配职位，没来的下线当人机踢了') # TODO: NOP

    print(' normal '.center(50, '-'))
    tokenize('good morning')
    tokenize('gogogo')
    tokenize('address')
    tokenize('加油加油加油')
    tokenize('收到')
    tokenize('课金')
    tokenize('测试123123123中')
    tokenize('111111')
    tokenize('hi 你也是刚玩的吗')

    print(' system info '.center(50, '-'))
    tokenize('进攻了光源村:进攻了光源村')
    tokenize('防守[刘邦算计]小老虎的進攻:防守*刘邦算计*小老虎的進攻')

    print(' emoji '.center(50, '-'))
    tokenize('chatemoji:7')

    print(' localization '.center(50, '-'))
    tokenize('{localization:519-473} 40w')
    tokenize('40w {localization:519-473}')

    print(' schedule message '.center(50, '-'))
    tokenize('{scheduleMsg:1618741814-郑}')

    print(' ads '.center(50, '-'))
    tokenize('50新币/150马币=6玩玉钰6万黄金+line：6888k') # TODO: NOP

    print(' contact '.center(50, '-'))
    tokenize('微信号多少？')
    tokenize('微信多少')
    tokenize('108给3万玉要加扣扣730356479')
    tokenize('有没有群')
    tokenize('∨')
    tokenize('群多少啊')
    tokenize('有赖吗')
    tokenize('我的line是dgjunon')
    tokenize('加我yao_0713')
    tokenize('lineid：sheung_kwan1321aaqqid:634676841加我们军团群的人请走这边～一天没上线会踢') # TODO: NOP
    tokenize('就你没十老大嶶信了')
    tokenize('stop_321')
    tokenize('line:kelvinchan8612')
    tokenize('z h e g u 9 0 8')
    tokenize('企鹅')
    tokenize('加团长徽：15183063671（梦瑶）我啦你们进群，领取对应的礼包码，不来的当机器人踢了')
    tokenize('你加我id')
    tokenize('911eo888')

    print(' add '.center(50, '-'))
    tokenize('怎么加')
    tokenize('我加你')
    tokenize('hi, 加入我们，一起玩吗')
    tokenize('你好呀，请问有机会加入我们吗')
    tokenize('我想加入你们')

    print(' vip '.center(50, '-'))
    tokenize('vip666666')
    tokenize('vip5个7')

    print(' resource '.center(50, '-'))
    tokenize('200多万资源')
    tokenize('资源爆满了')
    tokenize('有兑换码吗？')
    tokenize('有没有福利码')
    tokenize('礼包码是什么')
    tokenize('送资源送功勋了 {localization:254-451}')
    tokenize('ziyuan18972079820')
    tokenize('一百多万资源')
    tokenize('小号去拉资源 {localization:482-837}')
    tokenize('有要礼包的私下我')
    tokenize('theme:礼包码 content: 礼包码1heroccmm911eo888pin88888backccmmycbzq638769bqzze738975ccmtw0311') # TODO: NOP

    print(' transaction '.center(50, '-'))
    tokenize('*收')
    tokenize('selling call V 19888310671') # TODO: NOP
    tokenize('收的')

    print(' plugin '.center(50, '-'))
    tokenize('gogle搜寻春秋m辅助')

    print(' other game '.center(50, '-'))
    tokenize('三国志战略版')

    print(' abuse '.center(50, '-'))
    tokenize('cn')
    tokenize('cnm')
    tokenize('cnmlgb')
    tokenize('cnmlgbww')

    print(' audio '.center(50, '-'))
    tokenize('{audio:https://qxfzios-cdn-hz.himengyou.com/2021-06-08/2536.amr=5}')

    print(' url '.center(50, '-'))
    tokenize('https://baike.baidu.com')
