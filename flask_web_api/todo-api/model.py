from ex_login import db
from passlib.apps import custom_app_context as pwd_context
''''' 
创建类的时候继承UserMixin ,有一些用户相关属性 

* is_authenticated ：是否被验证 
* is_active ： 是否被激活 
* is_anonymous : 是否是匿名用户 
* get_id() : 获得用户的id，并转换为 Unicode 类型 

'''


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self,password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self,password):
        return pwd_context.verify(password,self.password_hash)
