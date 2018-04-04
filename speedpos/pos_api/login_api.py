import requests
from scrapy.selector import Selector
import pymysql
import json
import time
from flask import Flask
from flask import request,session,render_template
from flask import jsonify,abort
from flask_cors import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import functools

databaseurl = 'mysql://root:xhongc@localhost/info'
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)


    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

db.create_all()



def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in required_args:
                if arg not in request.form:
                    return jsonify(code=400, msg='参数不正确')
            return func(*args, **kw)
        return wrapper
    return decorator


@app.route('/login', methods=['POST'])
@require('username','password')
def login_api():

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        users= Users.query.filter_by(username=username).first()
        if password == users.password_hash:
            return 'Right'
    except:
        return 'eRROR'


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True)
