from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, current_user, login_user, login_required

app = Flask(__name__)
app.secret_key = 'Sqsdsffqrhgh.,/1#$%^&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xhongc@localhost/info'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

password = '123'  # 只要用户输入的密码是 123 就可以登录


@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
if __name__ == '__main__':
    app.run()