from app import api
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date
import logging
import time
import os
import sys

logger = logging.getLogger('request_handle')
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler("req.log")
logger.addHandler(fileHandler)
logger.info('----------')


@api.route('/suggestions/', methods=['POST'])
@login_required
@db_error_handling
def suggest():
    if not all((request.json.get('content'), request.json.get('contact'))):
        return jsonify({'message': 'args missing'}), 400
    s = Suggestion()
    s.user_id = Student.get_current().id
    s.time = date.today().isoformat()
    s.content = request.json.get('content')
    s.contact = request.json.get('contact')
    db.session.add(s)
    db.session.commit()
    return 'OK', 200


@api.before_request
def log_request():
    logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logger.info(request.method + ' ' + request.path)
    logger.info(request.cookies)
    logger.info(request.get_data())
    logger.info('----------')


# debug mode
@api.route('/restart/')
def restart_program():
    """Restarts the current program
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)
