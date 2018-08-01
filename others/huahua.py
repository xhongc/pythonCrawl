# with open(r'C:/test/110.txt', 'r') as f:
#     count = 0
#     for i in f.readlines():
#         res = i.split(' ')
#         # print(res)
#         item = []
#         for j in res:
#             if j:
#                 j = j.replace('\n','')
#                 item.append(j)
#         # print(item)
#         if len(item)>2:
#             count +=1
#             print("'%s':'%s',"%(item[0],item[-1]))
#     print(count)
def run():
    try:
        return '1'
    except:
        pass
    finally:
        return '2'

print(run())
