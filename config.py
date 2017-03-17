CSRF_ENABLED = True  # 激活CSRF保护
SECRET_KEY = "you-will-never-guess"  # 当CSRF激活的时候,建立一个加密的令牌,用于验证一个表单
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

OPENID_PROVIDERS = [
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'http://openid.org.cn' }]

# 邮箱服务器设置
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# 管理员表
ADMINS = ['you@example.com']