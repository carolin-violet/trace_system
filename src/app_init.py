from flask import Flask
from extension import db
from src.views import login, user, commodity, logistics
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('settings.Config')
cors = CORS(app, resources={'/*': {'origins': '*'}})
app.secret_key = 'yesyyds'

db.app = app
db.init_app(app)

app.register_blueprint(login.login_page)
app.register_blueprint(user.user_page)
app.register_blueprint(commodity.commodity_page)
app.register_blueprint(logistics.logistics_page)


if __name__ == '__main__':
    # 创建表
    db.create_all()
    app.run(host='0.0.0.0', port=6613)






