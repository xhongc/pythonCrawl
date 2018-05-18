
pools = ['1','2','-','3']
if '-' in pools:
    index_jian = pools.index('-')
    a = pools[:index_jian]
    b = pools[index_jian+1:]
    a = ''.join(a)
    b = ''.join(b)
    result = int(a) - int(b)
    print(result)