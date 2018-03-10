from  __init__ import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    # @property
    # def is_authenticated(self):
    #     return True
    # @property
    # def is_active(self):
    #     return True
    # @property
    # def is_anonymous(self):
    #     return False

    is_authenticated = True
    is_active = True
    is_anonymous = False
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<user %r>'%(self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<post %r>' %(self.body)