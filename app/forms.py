from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField  # 两个字段类
from wtforms.validators import DataRequired  # DataRequired验证器是检查提交的数据是否为空.


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
