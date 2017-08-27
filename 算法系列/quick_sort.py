def quick_sort(lists,l,r):
    if l >= r:
        return None
    low = l
    high = r
    key = lists[l]
    while l < r:
        while l<r and lists[r]> key:
            r-=1
        lists[l] = lists[r]
        lists[r] = key

        while l<r and lists[l]<=key: #此处为<=
            l+=1
        lists[r] =lists[l]
        lists[l] = key

    quick_sort(lists,low,l-1)
    quick_sort(lists,l+1,high)

lists =[11, 14, 10, 9, 6, 99, 16, 5, 1, 3, 2, 4, 1,1,1,1,1, 13, 26, 18,11, 2, 45, 34, 23, 1, 7, 3, 22, 19, 2]
quick_sort(lists,0,len(lists)-1)
print(lists)