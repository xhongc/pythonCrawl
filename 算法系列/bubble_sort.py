'''def bubble_sort(lists):
    count =0
    for j in range(len(lists)):
        for i in range(len(lists)-j-1):
            if lists[i]>lists[i+1]:
                lists[i],lists[i+1] = lists[i+1],lists[i]
            count+=1
        print(lists,count)
    print(lists)
lists=[21,5,6,1,8,99,56,34,12]
bubble_sort(lists)'''

def bubble_sort(lists):
    # 冒泡排序
    count = len(lists)
    for i in range(count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    print(lists)
lists=[21,5,6,1,8,99,56,34,12,2,44,55,66,5]
bubble_sort(lists)