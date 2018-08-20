import jieba.posseg as psg
import jieba
from collections import Counter

s = '我想和女朋友一起去北京故宫博物院参观和闲逛'
# cut = jieba.cut(s, cut_all=True)
# print(','.join(cut))
print([(x.word, x.flag) for x in psg.cut(s)])
