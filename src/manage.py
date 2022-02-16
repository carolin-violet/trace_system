from app_init import create_app
from flask_cors import CORS
from utils import table_init

app, db = create_app()
cors = CORS(app, resources={'/*': {'origins': '*'}})


# table_init.initialize(db)


@app.route('/', methods=['GET'])
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)


