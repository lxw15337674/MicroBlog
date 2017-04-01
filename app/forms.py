from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField,PasswordField  # 两个字段类
from wtforms.validators import DataRequired, Length, EqualTo  # DataRequired验证器是检查提交的数据是否为空.
from app.models import User


class LoginForm1(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class LoginForm2(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),Length(6, 12, message=u'密码长度在6到12')])
    remember_me = BooleanField('remember_me', default=False)


class registerForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),Length(6, 12, message=u'密码长度在6到12')])
    password1 = PasswordField(u'确认密码', validators=[DataRequired(), Length(6, 12, message=u'密码长度在6到12'), EqualTo('password', message=u'密码必须一致')])

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append("这个昵称已经被使用,请换其他的昵称")
            return False
        return True


class PostForm(FlaskForm):
    post = TextAreaField('post', validators=[DataRequired(message="发布的微博不能为空")])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
