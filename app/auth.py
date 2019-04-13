from app import api
from flask import request, jsonify
from app.models import *
from app import school
import requests


@api.route('/bind/', methods=['POST'])
def bind():
    # args required
    if not all([request.json.get('code'), request.json.get('stdnum'), request.json.get('password'),
                request.json.get('password')]):
        return jsonify({'message': 'args missing'}), 400
    # request wechat service
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                       params={'appid': 'wx99d261528d305c95',
                               'secret': '05d825b264778a54680bd07f708c176b',
                               'js_code': request.json.get('code'),
                               'grant_type': 'authorization_code'})

    if str(res.json()['errcode']) == '0':
        openid = res.json()['openid']
    else:
        return jsonify({'message': 'code2Session错误 ' + str(res.json()['errcode'])}), 400
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
    student.department_id = Department.query.filter_by(department_name=data['user']['deptName']).first().id
    dept = Department.query.get(student.department_id)
    dept.member += 1
    # save db
    db.session.add(student)
    db.session.add(dept)
    db.session.commit()
    return jsonify({'message': 'OK'}), 200


@api.route('/login/', methods=['POST'])
def login():
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                       params={'appid': 'wx99d261528d305c95',
                               'secret': '3fe3d64d1c5d5a17ddd4f8c6103368c4',
                               'js_code': request.json.get('code'),
                               'grant_type': 'authorization_code'})

    if str(res.json().get('errcode')) == '0':
        openid = res.json()['openid']
    else:
        return jsonify({'message': 'code2Session错误 ' + str(res.json())}), 400
    # verify
    student = Student.query.filter_by(openid=openid).first()
    if not student:
        return jsonify({'msg': 'Unauthorized'}), 401
    session['id'] = student.id
    data = {
        "id": student.id,
        "stdnum": student.stdnum if student.show_stdnum else '0',
        "openid": student.openid,
        "username": student.username,
        "qq": student.qq if student.show_qq else '0',
        "booknum": student.booknum,
        "department_id": student.department_id,
        "likes": student.likes
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
