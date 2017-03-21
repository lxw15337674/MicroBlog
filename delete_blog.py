# 删除blog
from app.models import Post
from app import db

for post in Post.query.all():
    db.session.delete(post)
db.session.commit()