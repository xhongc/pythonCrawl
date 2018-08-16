import jieba

seg_list = jieba.cut_for_search("有三个传奇的女性在古代被每一个人所熟知，帝王风范的武则天、吕雉、还有就是超级奢侈豪华的太后慈禧大人，")
print("Full Mode: " + "/ ".join(seg_list))
