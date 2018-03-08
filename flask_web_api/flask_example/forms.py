from flask_wtf import FlaskForm as Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid',validators=[DataRequired()])  # DataRequired 验证器只是简单地检查相应域提交的数据是否是空
    remember_me = BooleanField('remember_me',default = False)