import inspect


class APP(object):
    def case1(self):
        print('case1')

    def case2(self):
        return 'asd'

    def __repr__(self):
        class_name = type(self).__name__
        print(type(self))
        return '{}'.format(class_name)


def case1():
    print('aa')
    return 'haha'


# pro = [globals()[name] for name in globals() if name.startswith('case')]
# pro[0]()
# pro = [func for name, func in inspect.getmembers(APP, inspect.isfunction)]
# print(pro)
print(APP())
