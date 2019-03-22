from app import api
from flask import request, jsonify
from app.models import *


@api.route('/likes/', methods=['GET', 'POST', 'DELETE'])
@login_required
def likes():
    data = []
    student = Student.get_current()
    if request.method == 'GET':
        for item in Likes_lib.query.filter_by(visitor_id=student.id):
            data.append({
                'rank': 0,
                'star_id': item.star_id
            })
        for item in Likes_step_person.query.filter_by(visitor_id=student.id):
            data.append({
                'rank': 1,
                'star_id': item.star_id
            })
        for item in Likes_dep_daily.query.filter_by(visitor_id=student.id):
            data.append({
                'rank': 2,
                'star_id': item.star_id
            })
        for item in Likes_dep_weekly.query.filter_by(visitor_id=student.id):
            data.append({
                'rank': 3,
                'star_id': item.star_id
            })
        for item in Likes_dep_monthly.query.filter_by(visitor_id=student.id):
            data.append({
                'rank': 4,
                'star_id': item.star_id
            })
        return jsonify(data), 200
    elif request.method == 'POST':
        rank_id = int(request.form.get('type'))
        t = None
        if rank_id == 0:
            if Likes_lib.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_lib(visitor_id=student.id, star_id=request.form.get('star_id'))
        elif rank_id == 1:
            if Likes_step_person.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_step_person(visitor_id=student.id, star_id=request.form.get('star_id'))
        elif rank_id == 2:
            if Likes_dep_daily.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_daily(visitor_id=student.id, star_id=request.form.get('star_id'))
        elif rank_id == 3:
            if Likes_dep_weekly.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_weekly(visitor_id=student.id, star_id=request.form.get('star_id'))
        elif rank_id == 4:
            if Likes_dep_monthly.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_monthly(visitor_id=student.id, star_id=request.form.get('star_id'))
        if t:
            db.session.add(t)
            db.session.commit()
            return 'OK', 200
        else:
            return 'args error', 400
    elif request.method == 'DELETE':
        rank_id = int(request.form.get('type'))
        t = None
        if rank_id == 0:
            if not Likes_lib.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_lib.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first()
        elif rank_id == 1:
            if not Likes_step_person.query.filter_by(visitor_id=student.id,
                                                     star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_step_person.query.filter_by(visitor_id=student.id,
                                                      star_id=request.form.get('star_id')).first()
        elif rank_id == 2:
            if not Likes_dep_daily.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_daily.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first()
        elif rank_id == 3:
            if not Likes_dep_weekly.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_weekly.query.filter_by(visitor_id=student.id, star_id=request.form.get('star_id')).first()
        elif rank_id == 4:
            if not Likes_dep_monthly.query.filter_by(visitor_id=student.id,
                                                     star_id=request.form.get('star_id')).first():
                return 'already', 400
            else:
                t = Likes_dep_monthly.query.filter_by(visitor_id=student.id,
                                                      star_id=request.form.get('star_id')).first()
        if t:
            db.session.delete(t)
            db.session.commit()
            return 'OK', 200
        else:
            return 'args error', 400
