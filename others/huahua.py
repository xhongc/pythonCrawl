def buggy(arg, result=[]):
    print(result)
    result.append(arg)
    print(result)

buggy('a')
buggy('b')
buggy('c')