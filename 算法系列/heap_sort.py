'''
堆排序
'''
#调整每个堆 父节点大于子节点
def adjust_heap(lists,node,size):
    max = node
    lchild = 2 * node + 1
    rchild = 2* node +2
    if node < size//2:
        if lchild < size and lists[lchild] > lists[max]:
            max = lchild
        if rchild < size and lists[rchild] > lists[max]:
            max = rchild
        if max != node:  #运用递归对被破坏的结构重新排序
            lists[max],lists[node] = lists[node],lists[max]
            adjust_heap(lists,max,size)

def heap_sort(lists):
    size = len(lists)
    for i in range(0,size//2)[::-1]:
        adjust_heap(lists,i,size)
    for j in range(0,size)[::-1]: #一个个的弹出 堆顶最大值
        lists[0],lists[j] = lists[j],lists[0]
        adjust_heap(lists,0,j)

lists = [1,5,2,6,0,9,5,9,3,9,1]
heap_sort(lists)
print(lists)