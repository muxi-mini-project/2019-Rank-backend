import os
from flask import Flask
from app import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


base_dir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or b'apple'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Q110110110@localhost/rank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1")


if __name__ == '__main__':
    app.run(debug=True)
