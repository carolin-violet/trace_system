from flask import Flask
from models import db
from src.views import login, userInfo


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')

    app.secret_key = 'yesyyds'

    db.app = app
    db.init_app(app)

    # 创建表
    db.create_all()

    app.register_blueprint(login.api)
    app.register_blueprint(userInfo.api)

    return app







