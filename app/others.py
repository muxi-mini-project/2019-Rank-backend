from app import api
from flask import request
from app.model import *
from run import db
import time

@api.route('/suggestions', methods=['POST'])
@login_required
def suggest():
    s = Suggestion()
    s.user_id = Student.get_current().id
    lt = time.localtime()
    s.time = "{0}-{1}-{2}".format(lt.tm_year, lt.tm_mon, lt.tm_mday)
    s.content = request.form['content']
    s.contact = request.form['contact']
    db.session.add(s)
    db.session.commit()
    return 'OK', 200