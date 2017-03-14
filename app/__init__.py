from flask import Flask

app = Flask(__name__)
app.config.from_object('config') #读取配置文件
from app import views

if __name__ == '__main__':
    app.run()
