from app_init import create_app
from flask_cors import CORS


app, db, auth = create_app()
cors = CORS(app, resources={'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run()


