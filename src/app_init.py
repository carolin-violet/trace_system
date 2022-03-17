from flask import Flask
from flask_httpauth import HTTPBasicAuth

from models import db
from views import user, commodity, logistics, blockchain, produce, produce_th, purchase


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')
    auth = HTTPBasicAuth(app)

    db.app = app
    db.init_app(app)

    app.register_blueprint(user.user_page)
    app.register_blueprint(commodity.commodity_page)
    app.register_blueprint(logistics.logistics_page)
    app.register_blueprint(blockchain.chain_page)
    app.register_blueprint(produce.produce_page)
    app.register_blueprint(produce_th.produce_th_page)
    app.register_blueprint(purchase.purchase_page)
    return app, db, auth







