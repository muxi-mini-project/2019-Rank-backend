from app import api
from flask import request
from app.models import *
from run import db
from datetime import date


@api.route('/suggestions/', methods=['POST'])
@login_required
def suggest():
    s = Suggestion()
    s.user_id = Student.get_current().id
    s.time = date.today().isoformat()
    s.content = request.form.get('content')
    s.contact = request.form.get('contact')
    db.session.add(s)
    db.session.commit()
    return 'OK', 200
