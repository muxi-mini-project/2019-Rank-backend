from app import api, parse_isoformat_date
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date, timedelta


@api.route('/werun/', methods=['GET', 'POST'])
@login_required
def werun():
    if request.method == 'GET':
        start = parse_isoformat_date(request.args.get('start')) or date.today() - timedelta(days=15)
        end = parse_isoformat_date(request.args.get('end')) or date.today()
        student = Student.get_current()
        werun = WeRun.query.filter(WeRun.user_id == student.id, WeRun.time >= start, WeRun.time <= end)
        data = [{'time': x.time.isoformat(), 'step': x.step} for x in werun]
        return jsonify(data), 200
    elif request.method == 'POST':
        data = request.get_json()
        student = Student.get_current()
        for item in data:
            werun = WeRun()
            werun.user_id = student.id
            werun.time = date.fromtimestamp(int(item['timestamp']))
            werun.step = item['step']
            db.session.add(werun)
        db.session.commit()
        return 'OK', 200
