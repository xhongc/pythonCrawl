import re

f1 =  open(r'D:\test\ASP.TXT','r')
f2 = open(r'D:\test\editor.txt','a')
# for each in f1.readlines():
#     each = re.search('href="(.*?)"',each).group(1)
#     f2.write(each+'\n')
for each in f1.readlines():
    if 'editor' in each:
        f2.write(each)
f1.close()
f2.close()