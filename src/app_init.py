from flask import Flask
from models import db
from src.views import login, userInfo, articles, plans, diary, navigations


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')


    app.secret_key = 'zjyyds'

    db.app = app
    db.init_app(app)

    # 创建表
    db.create_all()

    app.register_blueprint(login.api)
    app.register_blueprint(userInfo.api)
    app.register_blueprint(articles.api)
    app.register_blueprint(plans.api)
    app.register_blueprint(diary.api)
    app.register_blueprint(navigations.api)
    return app







