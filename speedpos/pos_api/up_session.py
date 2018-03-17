import requests
from scrapy.selector import Selector
import json
import time
import random
import re
from flask import Flask
from flask import request, session
from flask import jsonify, abort
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flasgger.utils import swag_from



app = Flask(__name__)
swagger = Swagger(app)
# flask 解决跨域问题
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'xhc1950'

@swag_from('login.yml')
@app.route('/',methods=['GET','POST'])
def login():
    print(request.values.get('login_name'))
    if not request.values.get('login_name') and not request.values.get('login_pwd'):
        abort(400)
    return jsonify ({'code':request.values.get('login_name')})

if __name__ == '__main__':
    app.run(debug=True)