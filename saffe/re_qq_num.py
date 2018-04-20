import re

f1 = open('qun.txt','r',encoding='utf-8')
f2 = open('result.txt','a',encoding='utf-8')

for each in f1.readlines():
    try:
        each = re.search('([0-9]{6,11})',each).group(1)
        f2.write(each)
        f2.write('\n')
    except AttributeError:
        pass
f1.close()
f2.close()
