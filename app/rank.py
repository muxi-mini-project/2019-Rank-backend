from app import api
from flask import request, jsonify
from app.models import *
import math
import update

redis_db = update.redis_db


POSTS_PER_PAGE = 8


@api.route('/rank/lib')
@login_required
@db_error_handling
def lib():
    update.lib_rank()
    page = int(request.args.get('page') or 1)
    start = POSTS_PER_PAGE * (page - 1)
    end = POSTS_PER_PAGE * page - 1
    student = Student.get_current()
    data = {'total_page': math.ceil(redis_db.zcard('lib_rank') / POSTS_PER_PAGE),
            'now_page': page,
            'list': [],
            'my': {
                'rank': redis_db.zrevrank('lib_rank', student.id) + 1,
                'booknum': student.booknum,
                'user_id': student.id,
                'username': student.username,
                'url': student.avatar
            }}
    for uid in redis_db.zrevrange('lib_rank', start, end):
        student = Student.query.get(uid)
        data['list'].append({
            'booknum': student.booknum,
            'user_id': student.id,
            'username': student.username,
            'url': student.avatar
        })
    return jsonify(data), 200


@api.route('/rank/step/person')
@login_required
@db_error_handling
def step_person():
    update.step_person_rank()
    page = int(request.args.get('page') or 1)
    start = POSTS_PER_PAGE * (page - 1)
    end = POSTS_PER_PAGE * page - 1
    student = Student.get_current()
    data = {'total_page': math.ceil(redis_db.zcard('step_person_rank') / POSTS_PER_PAGE),
            'now_page': page,
            'list': [],
            'my': {
                'rank': redis_db.zrevrank('step_person_rank', student.id) + 1,
                'step': redis_db.zscore('step_person_rank', student.id),
                'user_id': student.id,
                'username': student.username,
                'url': student.avatar
            }}
    for uid, step in redis_db.zrevrange('step_person_rank', start, end, withscores=True):
        student = Student.query.get(uid)
        data['list'].append({
            'step': step,
            'user_id': student.id,
            'username': student.username,
            'url': student.avatar
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/week')
@db_error_handling
def dept_week():
    update.dep_weekly_rank()
    data = []
    for dept_id, step in redis_db.zrevrange('dep_weekly_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": int(dept_id),
            "department_name": Department.query.get(dept_id).department_name,
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/month')
@db_error_handling
def dept_month():
    update.dep_monthly_rank()
    data = []
    for dept_id, step in redis_db.zrevrange('dep_monthly_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": int(dept_id),
            "department_name": Department.query.get(dept_id).department_name,
        })
    return jsonify(data), 200
