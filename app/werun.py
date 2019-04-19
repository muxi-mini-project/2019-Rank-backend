from app import api, parse_isoformat_date
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date, timedelta
from WeChat.WXBizDataCrypt import WXBizDataCrypt


@api.route('/werun/', methods=['GET', 'POST'])
@login_required
@db_error_handling
def _werun():
    if request.method == 'GET':
        start = parse_isoformat_date(request.args.get('start') or (date.today() - timedelta(days=15)).isoformat())
        end = parse_isoformat_date(request.args.get('end') or date.today().isoformat())
        student = Student.get_current()
        werun = WeRun.query.filter(WeRun.user_id == student.id, WeRun.time >= start, WeRun.time <= end)
        data = [{'time': x.time.isoformat(), 'step': x.step} for x in werun]
        return jsonify(data), 200

    elif request.method == 'POST':
        student = Student.get_current()
        # decrypt data from WeChat
        encrypted_data = request.json.get('encryptedData')
        iv = request.json.get('iv')
        pc = WXBizDataCrypt('wx99d261528d305c95', student.session_key)
        data = pc.decrypt(encrypted_data, iv)

        for item in data["stepInfoList"]:
            t = date.fromtimestamp(int(item['timestamp']))
            werun = WeRun.query.filter_by(user_id=student.id, time=t).first()
            if werun:
                if werun.time == date.today():
                    werun.step = item['step']
            else:
                # create someday's info
                werun = WeRun()
                werun.user_id = student.id
                werun.time = t
                werun.step = item['step']
            db.session.add(werun)

        db.session.commit()
        return 'OK', 200
