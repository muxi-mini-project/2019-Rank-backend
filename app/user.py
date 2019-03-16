from app import api
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date


@api.route('/users/my/info', methods=['PUT', 'GET'])
@login_required
def myself():
    if request.method == 'PUT':
        student = Student.get_current()
        if request.form.get('qq'):
            student.qq = request.form.get('qq')
        student.show_qq = bool(int(request.form.get('show_qq'))) or False
        student.show_stdnum = bool(int(request.form.get('show_stdnum'))) or False
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'OK'}), 200

    elif request.method == 'GET':
        student = Student.get_current()
        data = student.__dict__.copy()
        data.pop('_sa_instance_state')
        data['department_name'] = Department.query.get(data['department_id']).department_name
        return jsonify(data), 200


@api.route('/users/<id>/info/')
def info(id):
    student = Student.query.get_or_404(id)
    werun = WeRun.query.filter_by(user_id=student.id,
                                 time=date.today().isoformat()).first()
    data = {
        "id": student.id,
        "stdnum": student.stdnum if student.show_stdnum else '0',
        "openid": student.openid,
        "username": student.username,
        "qq": student.qq if student.show_qq else '0',
        "booknum": student.booknum,
        "likes": student.likes,
        "step": werun.step if werun else 'null'
    }
    return jsonify(data), 200
