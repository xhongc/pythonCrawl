def insert_sort(lists):
    for index in range(1,len(lists)):
        key = lists[index]

        while index > 0 and lists[index-1] > key:
            lists[index] = lists[index-1]
            index -=1
        lists[index] = key

lists=[4,0,8,7,3,7,7,5,1,5,4,0]
insert_sort(lists)
print(lists)