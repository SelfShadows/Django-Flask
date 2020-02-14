from flask import Flask
from blue_print.views.account import ac
from blue_print.views.user import user_app


def create_app():
    app = Flask(__name__)
    app.register_blueprint(ac, url_prefix="/api")  # 加前缀
    app.register_blueprint(user_app)

    return app