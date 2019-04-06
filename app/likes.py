from app import api
from flask import request, jsonify
from app.models import *


@api.route('/likes/', methods=['GET', 'POST', 'DELETE'])
@login_required
def likes():
    student = Student.get_current()
    star_id = request.json.get('star_id') or request.args.get('star_id')
    is_liked = student.is_liked(star_id)

    if request.method == 'GET':
        stars = Likes.query.filter_by(star_id=star_id).count()
        return jsonify({
            'stars': stars,
            'is_liked': is_liked
        })

    elif request.method == 'POST':
        if is_liked:
            return jsonify({'msg': '已点赞'}), 400
        else:
            t = Likes(visitor_id=student.id, star_id=star_id)
            db.session.add(t)
            db.session.commit()
            return jsonify({'msg': 'OK'}), 200

    elif request.method == 'DELETE':
        if not is_liked:
            return jsonify({'msg': '已取消'}), 400
        else:
            t = Likes(visitor_id=student.id, star_id=star_id)
            db.session.delete(t)
            db.session.commit()
            return jsonify({'msg': 'OK'}), 200
