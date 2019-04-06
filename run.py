import os
from flask import Flask
from app import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import time

#time.sleep(10)

if not os.environ.get('SQLALCHEMY_DATABASE_URI'):
    raise ValueError('SQLALCHEMY_DATABASE_URI')
base_dir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or b'apple'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'), port=5000)
