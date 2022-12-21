from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_restplus import Api

from blue_prints.detect_api import detect_api, ns

import sys

sys.path.append("./blue_prints/detect")

app = Flask(__name__)

app.register_blueprint(detect_api, url_prefix="/detect_api")

bootstrap = Bootstrap(app)
CORS(app, supports_credentials=True)

api = Api(app, version='1.0', title='insects detection API',
          description='江苏大学iNetLab团队提供运维')

api.add_namespace(ns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
