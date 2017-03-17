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

from app import views,models

# 通过电子邮件发送错误
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PASSWORD,MAIL_PORT,MAIL_USERNAME
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME,MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# 启动日志记录
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
