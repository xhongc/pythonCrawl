def quick_sort(array, left, right):

    if left >= right:
        return
    low = left
    high = right
    key = array[low]  # 第一个值

    while low < high:  # 只要左右未遇见
        while low < high and array[high] > key:  # 找到列表右边比key大的值 为止
            high -= 1
        # 此时直接 把key(array[low]) 跟 比它大的array[high]进行交换
        array[low] = array[high]
        array[high] = key

        while low < high and array[low] <= key:  # 找到key左边比key大的值，这里为何是<=而不是<呢？你要思考。。。
            low += 1
            # array[low] =
        # 找到了左边比k大的值 ,把array[high](此时应该刚存成了key) 跟这个比key大的array[low]进行调换
        array[high] = array[low]
        array[low] = key

    quick_sort(array, left, low - 1)  # 最后用同样的方式对分出来的左边的小组进行同上的做法
    quick_sort(array, low + 1, right)  # 用同样的方式对分出来的右边的小组进行同上的做法


if __name__ == '__main__':
    array = [96, 14, 10, 9, 6, 99, 16, 5, 1, 3, 2, 4, 1, 13, 26, 18, 2, 45, 34, 23, 1, 7, 3, 22, 19, 2]
    # array = [8,4,1, 14, 6, 2, 3, 9,5, 13, 7,1, 8,10, 12]
    print("before sort:", array)
    quick_sort(array, 0, len(array) - 1)

    print("-------final -------")
    print(array)