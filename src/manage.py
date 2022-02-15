from app_init import create_app
from flask_cors import CORS

app = create_app()
cors = CORS(app, resources={'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)


