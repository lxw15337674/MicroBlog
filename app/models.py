from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    # 是否被认证
    def is_authenticated(self):
        return True

    # 是否有效,除非用户被禁止
    def is_active(self):
        return True

    # 是否匿名
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    #头像
    def avatar(self):
        return 'http://o7opur23b.bkt.clouddn.com/tuxiang.png'
    #打印
    def __repr__(self):
        return '<User %r>' % self.nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DATETIME)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body
