def shell_sort(lists):
    # 希尔排序
    count = len(lists)
    step = 2
    group = count // step
    while group > 0:
        for i in range(0, group):
            j = i + group
            while j < count:
                k = j - group
                key = lists[j]
                while k >= 0:
                    if lists[k] > key:
                        lists[k + group] = lists[k]
                        lists[k] = key
                    k -= group
                j += group
        group //= step
    return lists

lists = [1,5,2,6,0,9,5,9,2,9,1]
shell_sort(lists)
print(lists)