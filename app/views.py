from .date import date
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid, photos
from .models import User, Post
from .forms import LoginForm1, LoginForm2, SearchForm, EditForm, PostForm, registerForm, UploadForm
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from .emails import follower_notification


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=date(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash("你的消息已发布")
        return redirect(url_for('index'))
    # paginate 方法能够被任何查询调用。它接受三个参数:
    #     页数，从 1 开始，
    #     每一页的项目数，这里也就是说每一页显示的 blog 数，
    #     错误标志。如果是 True，当请求的范围页超出范围的话，一个 404 错误将会自动地返回到客户端的网页浏览器。如果是 False，返回一个空列表而不是错误。
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html",
                           title='Home',
                           form=form,
                           posts=posts)


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler  # 告诉Flask_openid这是登录视图函数
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form1 = LoginForm1()
    form2 = LoginForm2()
    if form1.validate_on_submit():
        session['remember_me'] = form1.remember_me.data
        return oid.try_login(form1.openid.data, ask_for=['nickname', 'email'])
    if form2.validate_on_submit():
        session['remember_me'] = form2.remember_me.data
        email = form2.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('该用户不存在')
        elif user.password != form2.password.data:
            flash('密码错误')
        else:
            login_user(user)
            flash("登陆成功")
            return redirect(url_for("/index"))
    return render_template('login.html',
                           title='Sign In',
                           form1=form1,
                           form2=form2,
                           providers=app.config['OPENID_PROVIDERS'])  # 注册页面


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            nickname=form.nickname.data,
            confirmed=True  # 这里默认验证,因为还没做邮箱认证系统
        )
        nickname = User.query.filter_by(nickname=user.nickname).first()
        if nickname is not None:
            flash("已存在的昵称,请更换其他的昵称")
            return redirect(url_for('register'))
        email = User.query.filter_by(nickname=user.email).first()
        if email is not None:
            flash("已注册的邮箱,请更换其他的邮箱")
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash('注册成功.')
        return redirect(url_for('register'))
    else:
        return render_template('register.html', form=form)


# 用户信息页
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash("不存在" + nickname + "用户")
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)


# 关注页面
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('用户 %s 没有找到.' % nickname)
        return redirect(url_for('index'))
    u = g.user.follow(user)
    if u is None:
        flash('不能关注' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('成功关注' + nickname + '!')
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


# 取消关注页面
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('用户 %s 没有找到.' % nickname)
        return redirect(url_for('index'))
    u = g.user.unfollow(user)
    if u is None:
        flash('不能取消关注 ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('已经取消关注' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


# 编辑页面
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('修改成功.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('edit.html', form=form)


# 头像上传
@app.route('/img', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data, folder='Avatar', name=g.user.nickname + '.')
        file_url = photos.url(filename)
        g.user.imgurl = file_url
        db.session.add(g.user)
        db.session.commit()
        flash('修改成功.')

    else:
        file_url = None
    return render_template('img.html', form=form, file_url=file_url)


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# 搜索
@app.route('/search,', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


# 测试bootstrap
@app.route('/test')
def test():
    return render_template('test.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('无效的登录,请重试')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email, confirmed=True, password=nickname)
        db.session.add(user)
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = date()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)


# 处理错误
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_errer(error):
    db.session.rollback()
    return render_template('500.html'), 500
