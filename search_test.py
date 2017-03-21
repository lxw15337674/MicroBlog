from app.models import User, Post
from app import db
import datetime

a =Post.query.whoosh_search('控件',like=True).all()
print(a)