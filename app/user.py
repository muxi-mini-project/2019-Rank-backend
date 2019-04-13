from app import api
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date
from app.school import get_books_num


@api.route('/users/my/info/', methods=['PUT', 'GET'])
@login_required
def myself():
    if request.method == 'PUT':
        student = Student.get_current()
        if request.json:
            json = request.json
        else:
            json = {}
        if json.get('qq'):
            student.qq = json.get('qq')
        student.show_qq = bool(int(json.get('show_qq') or 0))
        student.show_stdnum = bool(int(json.get('show_stdnum') or 0))
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'OK'}), 200

    elif request.method == 'GET':
        student = Student.get_current()
        werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
        data = {
            "id": student.id,
            "stdnum": student.stdnum,
            "openid": student.openid,
            "username": student.username,
            "qq": student.qq,
            "booknum": student.booknum,
            "department_id": student.department_id,
            "likes": student.likes,
            "step": werun.step if werun else 'null'
        }
        data['department_name'] = Department.query.get(data['department_id']).department_name
        return jsonify(data), 200


@api.route('/users/<id>/info/')
def info(id):
    student = Student.query.get_or_404(id)
    werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
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


@api.route('/users/my/info/avatar', methods=['PUT'])
@login_required
def my_avatar():
    student = Student.get_current()
    student.avatar = request.json.get('base64')
    db.session.add(student)
    db.session.commit()
    return "OK", 200


@api.route('/users/<id>/info/avatar')
@login_required
def get_avatar(id):
    student = Student.query.get_or_404(id)
    if student.avatar is None:
        return jsonify({'base64': 'null'}), 200
    else:
        return jsonify({'base64': student.avatar}), 200


@api.route('/users/lib/', methods=['POST'])
@login_required
def update_lib():
    student = Student.get_current()
    try:
        student.booknum = get_books_num(request.json.get('stdnum'), request.json.get('password'))
    except BaseException:
        student.booknum = 0
        return 'Bad Request', 400
    db.session.add(student)
    db.session.commit()
    return 'OK', 200
