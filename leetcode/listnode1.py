class Node():
    '创建节点'
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkList():
    '创建列表'
    def __init__(self, node):
        '初始化列表'
        self.head = node
        self.head.next = None
        self.tail = self.head

    def add_node(self, node):
        '添加节点'
        self.tail.next = node
        self.tail = self.tail.next

    def view(self):
        '查看列表'
        node = self.head
        link_str = ''
        while node is not None:
            if node.next is not None:
                link_str += str(node.data) + '-->'
            else:
                link_str += str(node.data)
            node = node.next
        print('The Linklist is:' + link_str)

    def length(self):
        '列表长度'
        node = self.head
        count = 1
        while node.next is not None:
            count += 1
            node = node.next
        print ('The length of linklist are %d' % count)
        return count

    def delete_node(self, index):
        '删除节点'
        if index+1 > self.length():
            raise IndexError('index out of bounds')
        num = 0
        node = self.head
        while True:
            if num == index-1:
                break
            node = node.next
            num += 1
        tmp_node = node.next
        node.next = node.next.next
        return tmp_node.data

    def find_node(self, index):
        '查看具体节点'
        if index+1 > self.length():
            raise IndexError('index out of bounds')
        num = 0
        node = self.head
        while True:
            if num == index:
                break
            node = node.next
            num += 1
        return node.data

node1 = Node(10)
node2 = Node('dec')
# node3 = Node(1010)
# node4 = Node('bin')
# node5 = Node(12)
# node6 = Node('oct')
# node7 = Node('A')
# node8 = Node('hex')
#
linklist = LinkList(node1)

linklist.add_node(node2)
# linklist.add_node(node3)
# linklist.add_node(node4)
# linklist.add_node(node5)
# linklist.add_node(node6)
# linklist.add_node(node7)
# linklist.add_node(node8)
#
# linklist.view()
# linklist.length()
# linklist.delete_node(1)
# linklist.view()
# find_node = linklist.find_node(6)
# print (find_node)

