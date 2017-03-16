from flask import Flask
app = Flask(__name__)
app.config.from_object('config') #读取配置文件

# 数据库
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 用户登录
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app,os.path.join(basedir,'tmp'))
#
from app import views,models



