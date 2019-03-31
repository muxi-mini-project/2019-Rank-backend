from app import api
from flask import request, jsonify
from app.models import *
from app import school
import requests


@api.route('/bind/', methods=['POST'])
def bind():
    # args required
    if not all([request.form.get('code'), request.form.get('stdnum'), request.form.get('password'),
                request.form.get('password')]):
        return jsonify({'message': 'args missing'}), 400
    # request wechat service
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                       params={'appid': 'wx99d261528d305c95',
                               'secret': '05d825b264778a54680bd07f708c176b',
                               'js_code': request.form.get('code'),
                               'grant_type': 'authorization_code'})

    if str(res.json()['errcode']) == '0':
        openid = res.json()['openid']
    else:
        return jsonify({'message': 'code2Session错误 ' + str(res.json()['errcode'])}), 400
    # is valid?
    student = Student.query.filter_by(openid=openid).first()
    if student:
        return jsonify({'message': '微信已经被注册'}), 400
    student = Student.query.filter_by(stdnum=request.form['stdnum']).first()
    if student:
        return jsonify({'message': '学号已经被注册'}), 400
    student = Student()
    data = school.login(request.form['stdnum'], request.form['password'])
    if not data:
        return jsonify({'message': '学号或密码错误'}), 400

    # set fields
    student.stdnum = request.form['stdnum']
    student.username = request.form['username']
    student.openid = openid
    student.department_id = Department.query.filter_by(department_name=data['user']['deptName']).first().id
    dept = Department.query.get(student.department_id)
    dept.member += 1
    # save db
    db.session.add(student)
    db.session.add(dept)
    db.session.commit()
    return jsonify({'message': 'OK'}), 200


# WIP
@api.route('/login/', methods=['POST'])
def login():
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                       params={'appid': 'wx99d261528d305c95',
                               'secret': '05d825b264778a54680bd07f708c176b',
                               'js_code': request.form.get('code'),
                               'grant_type': 'authorization_code'})

    if str(res.json()['errcode']) == '0':
        openid = res.json()['openid']
    else:
        return jsonify({'message': 'code2Session错误 ' + str(res.json()['errcode'])}), 400
    # verify
    student = Student.query.filter_by(openid=openid).first()
    if not student:
        return jsonify({'msg': 'Unauthorized'}), 401
    session['id'] = student.id
    data = student.__dict__.copy()
    data.pop('_sa_instance_state')
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
