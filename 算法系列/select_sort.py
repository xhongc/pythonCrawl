def select_sort(lists):
    length = len(lists)
    for i in range(length):
        min = i
        for j in range(i+1,length):
            if lists[i] > lists[j]:
                min = j
        lists[i],lists[min] = lists[min],lists[i]
    print(lists)

lists = [3,4,7,1,9,28,8]
select_sort(lists)