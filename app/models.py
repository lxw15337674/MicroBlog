from app import db, app
import flask_whooshalchemyplus

# 关注表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    # 设置与followers表的一对多关系
    followed = db.relationship('User',
                               secondary=followers,  # 指明这种关系的辅助表
                               primaryjoin=(followers.c.follower_id == id),  # 辅助表中连接左边实体(发起关注的用户)的条件.
                               secondaryjoin=(followers.c.followed_id == id),  # 辅助表中连接右边实体(被关注的用户)的条件
                               backref=db.backref('followers', lazy='dynamic'),
                               # 定义这种关系将如何从右边实体进行访问.当我们做出一个名为 followed 的查询的时候，将会返回所有跟左边实体联系的右边的用户。当我们做出一个名为 followers 的查询的时候，将会返回一个所有跟右边联系的左边的用户。lazy 指明了查询的模式,dynamic 模式表示直到有特定的请求才会运行查询
                               lazy='dynamic')  # 应用于常规查询。

    # 设置昵称,处理昵称相同的情况
    # @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

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

    # 头像
    def avatar(self):
        return 'http://o7opur23b.bkt.clouddn.com/tuxiang.png'

    # 查询返回所有当前用户作为关注者的 (follower, followed) 对。
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # 添加关注者
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # 移除关注者
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def followed_posts(self):
        # join连接,filter过滤,order_by排序
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    # 打印
    def __repr__(self):
        return '<User %r>' % self.nickname


class Post(db.Model):
    # 设置数据库中的所有能被搜索并且建立索引的字段
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body


# 通过调用 whoosh_index 函数，初始化了全文搜索索引。
flask_whooshalchemyplus.whoosh_index(app, Post)
