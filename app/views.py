from flask import render_template, flash, redirect
from .forms import LoginForm

from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [
        {
            'author': {'nickname': 'lixiwang'},
            'body': '星期二'
        },
        {
            'author': {'nickname': 'susan'},
            'body': '今天白天多云'
        }
    ]
    return render_template("index.html",
                           posts=posts,
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')

    return render_template("login.html",
                           title="登录",
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
