import os
import sys
from flask import Flask
from app import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

base_dir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1")

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    app.run(debug=True, host='127.0.0.1', port=5000)
    # app.run(debug=True, host='0.0.0.0', ssl_context=('rank.pem', 'rank.key'), port=5000)
