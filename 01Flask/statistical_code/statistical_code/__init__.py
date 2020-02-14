from flask import Flask
from redis import Redis
from flask_session import Session
import settings
from statistical_code.views.account import account
from statistical_code.views.index import ind
from statistical_code.views.tmp import my_tmp


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)  # 加载配置文件

    # session使用redis三步
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(host='192.168.52.128', port=6379, password='xiaoli')
    Session(app)

    app.register_blueprint(account)  # 导入蓝图
    app.register_blueprint(ind)  # 导入蓝图
    app.register_blueprint(my_tmp)  # 导入蓝图

    return app
