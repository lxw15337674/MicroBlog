from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField  # 两个字段类
from wtforms.validators import DataRequired, Length  # DataRequired验证器是检查提交的数据是否为空.


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
