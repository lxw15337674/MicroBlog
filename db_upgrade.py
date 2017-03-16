# 用于当数据库模型发生变化时,更新数据库
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO)
print('Current database version: '+str(api.db_version(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO)))