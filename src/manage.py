from app_init import create_app
from flask_cors import CORS


app, db = create_app()
cors = CORS(app, resources={'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def hello():
    return 'hello'


if __name__ == '__main__':
    # ip和端口在右上角pycharm右上角配置的,如 --host=127.0.0.1 --port=5000
    app.run()


