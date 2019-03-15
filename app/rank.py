from app import api
from flask import request, jsonify
from app.models import *
from run import db
import redis

redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=1)


@api.route('/rank/lib')
def lib():
    offset = int(request.args.get('offset') or 0)
    limit = int(request.args.get('limit') or 10)
    l = list()
    for uid in redis_db.zrevrange('lib_rank', offset, offset + limit):
        student = Student.query.get(uid)
        l.append({
            'booknum': student.booknum,
            'user_id': student.id,
            'username': student.username,
            'likes': Likes_lib.query.filter_by(star_id=student.id).count()
        })
    return jsonify(l), 200
