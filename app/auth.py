from app import api
from flask import request, jsonify
from app.models import *
from app import school_login


@api.route('/register/', methods=['POST'])
def register():
    try:
        # is valid?
        student = Student.query.filter_by(openid=request.form['openid']).first()
        if student:
            return jsonify({'message': '微信已经被注册'}), 400
        student = Student.query.filter_by(stdnum=request.form['stdnum']).first()
        if student:
            return jsonify({'message': '学号已经被注册'}), 400
        student = Student()
        data = school_login.login(request.form['stdnum'], request.form['password'])
        if not data:
            return jsonify({'message': '学号或密码错误'}), 400
        # set fields
        student.stdnum = request.form['stdnum']
        student.username = request.form['username']
        student.openid = request.form['openid']
        student.department_id = Department.query.filter_by(department_name=data['user']['deptName']).first().id
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'OK'}), 200
    except KeyError as e:
        return jsonify({'message': str(e)}), 400


# WIP
@api.route('/login/', methods=['POST'])
def login():
    code = request.form['code']
    # verify
    session['id'] = code
    student = Student.query.filter_by(id=request.form['code']).first()
    data = student.__dict__.copy()
    data.pop('_sa_instance_state')
    data['department_name'] = Department.query.get(data['department_id']).department_name
    return jsonify(data), 200
