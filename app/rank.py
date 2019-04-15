from app import api
from flask import request, jsonify
from app.models import *
import redis
import math

redis_db = redis.StrictRedis(host="redis", port=6379, db=1)

import app.update

app.update.main()
POSTS_PER_PAGE = 5


@api.route('/rank/lib')
@login_required
@db_error_handling
def lib():
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
            }}
    for uid in redis_db.zrevrange('lib_rank', start, end):
        student = Student.query.get(uid)
        data['list'].append({
            'booknum': student.booknum,
            'user_id': student.id,
            'username': student.username,
        })
    return jsonify(data), 200


@api.route('/rank/step/person')
@login_required
@db_error_handling
def step_person():
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
            }}
    for uid, step in redis_db.zrevrange('step_person_rank', start, end, withscores=True):
        student = Student.query.get(uid)
        data['list'].append({
            'step': step,
            'user_id': student.id,
            'username': student.username,
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/week')
@db_error_handling
def dept_week():
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
    data = []
    for dept_id, step in redis_db.zrevrange('dep_monthly_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": int(dept_id),
            "department_name": Department.query.get(dept_id).department_name,
        })
    return jsonify(data), 200
