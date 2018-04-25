import re

f1 =  open(r'D:\test\urls.txt','r')
f2 = open(r'D:\test\ok_urls.txt','a')
for each in f1.readlines():
    each = re.search('href="(.*?)"',each).group(1)
    f2.write(each+'\n')

f1.close()
f2.close()