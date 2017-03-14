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
    return render_template("login.html",
                           title="登录",
                           form=form)
