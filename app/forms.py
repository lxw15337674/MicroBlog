from flask_wtf.file import FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, FileField  # 两个字段类
from wtforms.validators import DataRequired, Length, EqualTo, Email  # DataRequired验证器是检查提交的数据是否为空.

from app import photos
from app.models import User


class LoginForm1(FlaskForm):
    openid = StringField('openid', validators=[DataRequired(message="不能为空")])
    remember_me = BooleanField('remember_me', default=False)


class LoginForm2(FlaskForm):
    email = StringField('email', validators=[DataRequired(message="不能为空"), Email(message="请输入正确的邮箱格式")])
    password = PasswordField('password', validators=[DataRequired(message="不能为空"), Length(6, 12, message=u'密码长度在6到12')])
    remember_me = BooleanField('remember_me', default=False)


class registerForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired(message="不能为空")])
    email = StringField('email', validators=[DataRequired(message="不能为空"), Email(message="请输入正确的邮箱格式")])
    password = PasswordField('password', validators=[DataRequired(message="不能为空"), Length(6, 12, message=u'密码长度在6到12')])
    password1 = PasswordField(u'确认密码', validators=[DataRequired(message="不能为空"), Length(6, 12, message=u'密码长度在6到12'),
                                                   EqualTo('password', message=u'密码必须一致')])


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired(message="不能为空")])
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
    search = StringField('search', validators=[DataRequired(message="搜索不能为空")])


class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])
