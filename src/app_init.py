from flask import Flask
from models import db
from views import user, commodity, logistics, blockchain, produce, th, sale, statistics


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')

    db.app = app
    db.init_app(app)

    app.register_blueprint(user.user_page)
    app.register_blueprint(commodity.commodity_page)
    app.register_blueprint(logistics.logistics_page)
    app.register_blueprint(blockchain.chain_page)
    app.register_blueprint(produce.produce_page)
    app.register_blueprint(th.th_page)
    app.register_blueprint(sale.sale_page)
    app.register_blueprint(statistics.statistics_page)
    return app, db







