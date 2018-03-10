from flask import render_template,redirect,flash,session,url_for,request,g
from flask import Flask
from forms import LoginForm
from flask_login import login_user,logout_user,current_user,login_required,LoginManager
from __init__ import app,db,login_manager,oid
from forms import LoginForm
from models import User

app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/index')
@app.route('/')
@login_required
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title ='HOME',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # return redirect('/index')
        session['remember_me'] = form.openid.data
        return oid.try_login(form.openid.data,ask_for=['nickname','email'])
    return render_template('login.html',
                           title = "sign in",
                           form = form,
                          providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email =='':
        flash('Invailid login ,please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname =='':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname,email = resp.email)
        db.session.add(user)
        db.session.commit()
        remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me',None)
    login_user(user,remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.run(debug=True)