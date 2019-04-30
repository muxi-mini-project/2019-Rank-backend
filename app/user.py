from app import api
from flask import request, jsonify
from app.models import *
from run import db
from datetime import date
from app.school import get_books_num
from app.rank import redis_db
import math
import update


@api.route('/users/my/info/', methods=['PUT', 'GET'])
@login_required
@db_error_handling
def myself():
    update.main()
    if request.method == 'PUT':
        student = Student.get_current()
        if request.json.get('qq'):
            student.qq = request.json.get('qq')
        if request.json.get('username'):
            student.username = request.json.get('username')
        student.show_qq = bool(int(request.json.get('show_qq') or 0))
        student.show_stdnum = bool(int(request.json.get('show_stdnum') or 0))
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'OK'}), 200

    elif request.method == 'GET':
        student = Student.get_current()
        werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
        rank = redis_db.zrevrank('step_person_rank', student.id)
        if rank is not None:
            rank += 1
        data = {
            "id": student.id,
            "stdnum": student.stdnum,
            "openid": student.openid,
            "username": student.username,
            "qq": student.qq,
            "booknum": student.booknum,
            "department_id": student.department_id,
            "likes": student.likes(),
            "step": werun.step if werun else 'null',
            "show_qq": student.show_qq,
            "show_stdnum": student.show_stdnum,
            "url": student.avatar,
            "rank": rank if rank else 'null',
            "contribute": 100 - 10 * math.floor(10 * redis_db.zrevrank('step_person_rank', student.id) /
                                                redis_db.zcard('step_person_rank')) if rank else 'null'
        }
        data['department_name'] = Department.query.get(data['department_id']).department_name
        return jsonify(data), 200


@api.route('/users/<id>/info/')
@login_required
@db_error_handling
def info(id):
    update.main()
    student = Student.query.get_or_404(id)
    werun = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first()
    rank = redis_db.zrevrank('step_person_rank', student.id)
    if rank is not None:
        rank += 1
    data = {
        "id": student.id,
        "stdnum": student.stdnum if student.show_stdnum else False,
        "openid": student.openid,
        "username": student.username,
        "qq": student.qq if student.show_qq else False,
        "booknum": student.booknum,
        "url": student.avatar,
        "likes": student.likes(),
        "is_liked": Student.get_current().is_liked(id),
        "step": werun.step if werun else 'null',
        "rank": rank if rank else 'null',
        "contribute": 100 - 10 * math.floor(10 * redis_db.zrevrank('step_person_rank', student.id) /
                                            redis_db.zcard('step_person_rank')) if rank else 'null'
    }
    return jsonify(data), 200


@api.route('/users/my/info/avatar', methods=['PUT'])
@login_required
@db_error_handling
def my_avatar():
    student = Student.get_current()
    student.avatar = request.json.get('url')
    db.session.add(student)
    db.session.commit()
    return "OK", 200


@api.route('/users/<id>/info/avatar')
@db_error_handling
def get_avatar(id):
    student = Student.query.get_or_404(id)
    if student.avatar is None:
        return jsonify({'url': 'null'}), 200
    else:
        return jsonify({'url': student.avatar}), 200


@api.route('/users/lib/', methods=['POST'])
@login_required
@db_error_handling
def update_lib():
    if not all((request.json.get('stdnum'), request.json.get('password'))):
        return jsonify({'message': 'args missing'}), 400
    student = Student.get_current()
    try:
        student.booknum = get_books_num(request.json.get('stdnum'), request.json.get('password'))
    except ValueError:
        student.booknum = 0
        return jsonify({'message': '您输入的用户名或密码有误'}), 400
    except ConnectionError:
        student.booknum = 0
        return jsonify({'message': 'ConnectionError'}), 500
    db.session.add(student)
    db.session.commit()
    return 'OK', 200
