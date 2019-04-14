from app import api
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date


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
