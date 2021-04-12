# encoding: utf-8

import os
import torch
import pickle
import numpy as np

from transformers     import BertTokenizer
from torch.utils.data import DataLoader
from .model           import BERTClass
from .dataset         import CustomDataset


# import torch
# import transformers
# 
# 
# class BERTClass(torch.nn.Module):
# 
#     def __init__(self):
#         super(BERTClass, self).__init__()
#         self.l1 = transformers.BertModel.from_pretrained(model_name)
#         self.l2 = torch.nn.Dropout(0.3)
#         self.l3 = torch.nn.Linear(768, len(mlb.classes_))
# 
# 
#     def forward(self, ids, mask, token_type_ids):
#         output_1 = self.l1(ids, attention_mask = mask, token_type_ids = token_type_ids)
#         output_2 = self.l2(output_1.pooler_output)
#         output = self.l3(output_2)
#         return output


path = os.path.dirname(__file__)
print(path)

with open(os.path.join(path,'model/mlb.pkl'), 'rb') as f:
    mlb = pickle.load(f)


model_name = 'hfl/chinese-bert-wwm-ext'
tokenizer = BertTokenizer.from_pretrained(model_name)


# model_file = os.path.join(path, 'model/chinese-bert-wwm-ext-4-cpu.bin')
# model = torch.load(model_file)

state_file = os.path.join(path, 'model/chinese-bert-wwm-ext-4-cpu.sd')
model = BERTClass(model_name, mlb)
model.load_state_dict(torch.load(state_file))

MAX_LEN = 512
BATCH_SIZE = 4


def predict(X):

    """ trian loader """
    dataset = CustomDataset(X, tokenizer, MAX_LEN)

    params = {
        'batch_size': BATCH_SIZE,
        'shuffle': False,
        'num_workers': 0}

    data = DataLoader(dataset, **params)

    y_pred = []
    
    """ predict """
    for _, d in enumerate(data, 0):
        
        # X
        ids = d['ids']
        mask = d['mask']
        token_type_ids = d['token_type_ids']
        
        # y_pred
        outputs = model(ids, mask, token_type_ids).detach().numpy()
        y_pred.extend((outputs >= 0.5).astype(int))

    """ to label """
    y_pred = mlb.inverse_transform(np.array(y_pred))
    return y_pred



if __name__ == '__main__':

    X = ["\n\n玩了三个区，加了好几次同盟，要求加微信，一加微信都问玩不玩其他游戏 喵喵喵！？？感情这游戏是"
    "用来打广告的？希望官方管管，月卡我也不要了，暂时不想玩这游戏了",
    
    "\n\n玩了差不多一个月了，这两天游戏里的汉家松鼠让我评论，那么我就来评一评。游戏立意不错，也是用心做了的，跟"
    "世面上很多以圈钱为目标开发的游戏是不同的。\n前期不错，我玩的很休闲，目前还没满级，所以很多评论里的bug我还"
    "没体验到。\n不过我觉得游戏升级太快，很多都不能慢慢体验，建议海市蜃楼经验取消，因为我想慢慢升级。\n不满意当"
    "然有很多，开发团队忘了初衷，试图把玩家绑在游戏上，每天的挑战本，抱歉我就打过几次，还有无尽的刷boss,打卡般"
    "的游戏活动。氖金也不厚道，体验完全公平版本的游戏，得铁粉才行，我这首充加月卡的，有些地方不能挂，还好我几乎当单"
    "机玩的，vip系统，呵呵呵，所以这游戏良心是没有的。\n总结一下，这游戏是有着做好游戏的初衷，看着周围一大群国"
    "产圈钱游戏，然后不淡定了。于是就成了食之别扭，弃之可惜。\n就这样，开发组一心忘了游戏的初衷，试图效仿资本，前"
    "不久玩了万达的游戏，果然是房地产商，心黑无底线。松鼠们你们会和万达比吗？\n用心做好游戏，是可以翻身的，因为国"
    "内烂游太多了。然而现在松鼠向着国内同行看齐，那么你们就和他们去泥地里打滚竞争吧。\n最后还是希望这游戏会更好吧"
    "，虽然我有很多不满，这游戏还是比国内大部分好，推荐玩。",
    
    "\n一年前我给的五星？（对不起我是穷逼，我只氪了500RMB，实在玩不动，对不起＞人＜策划大大）\n时隔一年多"
    "，修改下吧，本来眼前一亮的游戏，让游戏策划玩成了一坨✘。\n本来以为是个策略向游戏~没想到吃相越来越难看。\n"
    "70%的角色都要钱买，80%的关卡地图都要钱解锁😂好吧官方说了，可以0氪通关什么的，真的是放屁。\n一个地图或"
    "者一个英雄，一个章节基本都是200或300金币，除了刚进来关注微信，朋友圈什么的赚个200还要都用来解锁章节，"
    "剩下一天只能领5金币。攒两个月才够一个英雄或者解锁一章新章节就算如此我连续签到一年也只能够勉强解锁章节而已。\n"
    "什么英雄都没有你买你照样卡关，前一两章让你产生错觉，第三章的智熄难度让你怀疑人生~0氪再签到一年买了英雄，结"
    "果呢？没有一身红装你能过得了第三章？能过的了卧龙出山？！\n继续肝，再肝一年凑齐一身基础的红装，呵呵，你连赤壁"
    "之战都进不去。\n没有精炼出极品属性你连人物技能需要的属性点都凑不齐…至于装备多孔，精炼属性，红装宝箱¬_¬｀金币锁定"
    "其中一个属性什么的垃圾网游的逼氪套路不用我详细说了吧？0氪继续靠签到，一天5金币，除此以外没有给你任何刷东西变强的途径"
    "。起步一年，看你欧不欧吧，运气不好签到十年大概够你把你的红装精炼出合适的属性。\n这时候你以为努力终于有回报了，进图一"
    "波，照样怀疑人生~出来求问，哦，原来一身红装还不行，还得是帝剑火扇这个级别的“终极红装”才行！没事，官方说零氪可以通的"
    "，继续肝，又一个十年过去了……\n这个时候你以为终于可以把章节推到中期了！毕竟官方攻略上都说了，这样肯定是可以通关的。"
    "你带着满身终极神装冲向boss，自信满满的A了上去，然后自信满满的打出GG……\n咦？不对啊？按攻略一步步来的，装备也"
    "已经肝无可肝了，咋回事呢！？小伙伴们仔细研究~原来，GM大大把数据改了呢~毕竟都要恰饭的，原来的装备不弱化，boss不"
    "加强，大家怎么继续充钱啊？😂😂😂😂😂\n还好我并不是0氪党，我还没有肝进去***…不过这不就是令人智熄的策划大大的目的"
    "吗？两个字---逼氪。\n总的来说是一手好牌打的稀烂，挺好的一个游戏和创意，遇上了一很✘✘的策划……别入坑。"]


    y_pred = predict(X * 2)

    print(y_pred)
    # print(y_pred.shape)
