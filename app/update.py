from app.rank import *
import json


def lib_rank():
    redis_db.delete('lib_rank')
    for student in Student.query.all():
        redis_db.zadd('lib_rank', {student.id: student.booknum})
