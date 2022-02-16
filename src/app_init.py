from flask import Flask
from models import db
from views import login, user, commodity, logistics


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')

    db.app = app
    db.init_app(app)

    app.register_blueprint(login.login_page)
    app.register_blueprint(user.user_page)
    app.register_blueprint(commodity.commodity_page)
    app.register_blueprint(logistics.logistics_page)
    return app, db







