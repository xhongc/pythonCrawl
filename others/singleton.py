'''
元类（metaclass）可以控制类的创建过程

class Singleton(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance['ins'] = super(Singleton, cls).__call__(*args,**kwargs)
        return cls._instance['ins']
class Myclass(metaclass=Singleton):
    pass

a=Myclass()
b=Myclass()

print(id(a),id(b))
'''
'''
为了使类只能出现一个实例，我们可以使用 __new__ 来控制实例的创建过程
class Singleton(object):
    _ton = None
    def __new__(cls,*args,**kwargs):
        if not cls._ton:
            cls._ton = super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._ton
class Myclass(Singleton):
    pass
a=Myclass()
b=Myclass()

print(id(a),id(b))
'''
#使用装饰器
def singleton(cls):
    _ton = {}
    def wrapper(*args,**kwargs):
        if not _ton:
            _ton['cls'] = cls(*args,**kwargs)
        return _ton['cls']
    return wrapper

@singleton
class Myclass(object):
    pass
a=Myclass()
b=Myclass()

print(id(a),id(b))