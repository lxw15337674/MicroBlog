import os
from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, imgurl

app = Flask(__name__)
app.config.from_object('config')  # 读取配置文件

bootstrap = Bootstrap(app)

# 邮件
mail = Mail(app)

# 数据库
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 用户登录
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# 通过电子邮件发送错误
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure',
                               credentials)
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

#图片上传
app.config['UPLOADED_PHOTOS_DEST'] = imgurl #图片上传位置
photos = UploadSet('photos', IMAGES) #图片上传格式
configure_uploads(app, photos)
patch_request_class(app)    #设置图片最大空间,默认16MB

from app import views, models
