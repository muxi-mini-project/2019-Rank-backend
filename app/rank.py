# call Update function before rank !!!
from app import api
from flask import request, jsonify
from app.models import *
import redis

redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=1)


@api.route('/rank/lib')
def lib():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 10)
    data = list()
    for uid in redis_db.zrevrange('lib_rank', offset, offset + limit):
        student = Student.query.get(uid)
        data.append({
            'booknum': student.booknum,
            'user_id': student.id,
            'username': student.username,
            'likes': Likes_lib.query.filter_by(star_id=student.id).count()
        })
    return jsonify(data), 200


@api.route('/rank/step/person')
def step_person():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 10)
    data = list()
    for uid, step in redis_db.zrevrange('step_person_rank', offset, offset + limit, withscores=True):
        student = Student.query.get(uid)
        # step = WeRun.query.filter_by(user_id=student.id, time=date.today().isoformat()).first().step
        data.append({
            'step': step,
            'user_id': student.id,
            'username': student.username,
            'likes': Likes_step_person.query.filter_by(star_id=student.id).count()
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/today')
def dept_today():
    data = []
    for dept_id, step in redis_db.zrevrange('dep_daily_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": dept_id,
            "department_name": Department.query.get(dept_id).department_name,
            "likes": Likes_dep_daily.query.filter_by(star_id=dept_id).count()
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/week')
def dept_week():
    data = []
    for dept_id, step in redis_db.zrevrange('dep_weekly_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": dept_id,
            "department_name": Department.query.get(dept_id).department_name,
            "likes": Likes_dep_weekly.query.filter_by(star_id=dept_id).count()
        })
    return jsonify(data), 200


@api.route('/rank/step/dept/month')
def dept_month():
    data = []
    for dept_id, step in redis_db.zrevrange('dep_monthly_rank', 0, -1, withscores=True):
        data.append({
            "step": step,
            "department_id": dept_id,
            "department_name": Department.query.get(dept_id).department_name,
            "likes": Likes_dep_monthly.query.filter_by(star_id=dept_id).count()
        })
    return jsonify(data), 200