from app import api
from flask import request, jsonify
from app.models import *
from app import school
import requests


def code2session(code):
    # request WeChat service
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                       params={
                           'appid': 'wx99d261528d305c95',
                           'secret': '3fe3d64d1c5d5a17ddd4f8c6103368c4',
                           'js_code': code,
                           'grant_type': 'authorization_code'
                       })
    if res.json().get('errcode') is None:
        openid = res.json()['openid']
        session_key = res.json()['session_key']
        return openid, session_key
    else:
        return None, res.text


@api.route('/bind/', methods=['POST'])
@db_error_handling
def bind():
    # args checking
    if not all((request.json.get('code'), request.json.get('stdnum'), request.json.get('password'),
                request.json.get('username'))):
        return jsonify({'message': 'args missing'}), 400

    # request WeChat service
    openid, session_key = code2session(request.json.get('code'))
    if openid is None:
        return jsonify({'message': 'code2Session错误 ' + session_key}), 400

    # is valid?
    student = Student.query.filter_by(openid=openid).first()
    if student:
        return jsonify({'message': '微信已经被注册'}), 400
    student = Student.query.filter_by(stdnum=request.json['stdnum']).first()
    if student:
        return jsonify({'message': '学号已经被注册'}), 400
    student = Student()
    data = school.login(request.json['stdnum'], request.json['password'])
    if not data:
        return jsonify({'message': '学号或密码错误'}), 400

    # set fields
    student.stdnum = request.json['stdnum']
    student.username = request.json['username']
    student.openid = openid
    student.session_key = session_key
    student.department_id = Department.query.filter_by(department_name=data['user']['deptName']).first().id
    dept = Department.query.get(student.department_id)
    dept.member += 1
    # save db
    db.session.add(student)
    db.session.add(dept)
    db.session.commit()
    session['id'] = Student.query.filter_by(stdnum=request.json['stdnum']).first().id
    return jsonify({'message': 'OK'}), 200


@api.route('/login/', methods=['POST'])
@db_error_handling
def login():
    if not (request.json.get('code')):
        return jsonify({'message': 'args missing'}), 400

    # request WeChat service
    openid, session_key = code2session(request.json.get('code'))
    if openid is None:
        return jsonify({'message': 'code2Session错误 ' + session_key}), 400

    # verify
    student = Student.query.filter_by(openid=openid).first()
    if not student:
        return jsonify({'message': 'Unauthorized. Not registered.'}), 401
    else:
        student.session_key = session_key
        db.session.add(student)
        db.session.commit()
    session['id'] = student.id
    data = {
        "id": student.id,
        "stdnum": student.stdnum,
        "openid": student.openid,
        "username": student.username,
        "qq": student.qq,
        "booknum": student.booknum,
        "department_id": student.department_id,
        "likes": student.likes()
    }
    data['department_name'] = Department.query.get(data['department_id']).department_name

    return jsonify(data), 200


@api.route('/check/')
@login_required
def check():
    return 'OK', 200


# debug mode
@api.route('/jump/<id>')
def jump(id):
    session['id'] = id
    return 'OK', 200
