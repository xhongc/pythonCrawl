dict1 = {'a':1,'c':2,'b':3,'e':0}
#print(dict1.items())
dict1 = sorted(dict1.items(),key=lambda a:a[0],reverse=False)
print(dict1)