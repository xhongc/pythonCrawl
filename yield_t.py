def g(x):
    yield from range(x,0,-1)

list1 = list(g(5))
print (list1)