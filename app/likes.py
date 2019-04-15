from app import api
from flask import request, jsonify
from app.models import *


@api.route('/likes/', methods=['POST', 'DELETE'])
@login_required
@db_error_handling
def likes():
    student = Student.get_current()
    star_id = request.args.get('star_id') or request.json.get('star_id')
    is_liked = student.is_liked(star_id)

    if request.method == 'POST':
        if is_liked:
            return jsonify({'message': '已点赞'}), 400
        else:
            t = Likes(visitor_id=student.id, star_id=star_id)
            db.session.add(t)
            db.session.commit()
            return jsonify({'message': 'OK'}), 200

    elif request.method == 'DELETE':
        if not is_liked:
            return jsonify({'message': '已取消'}), 400
        else:
            t = Likes(visitor_id=student.id, star_id=star_id)
            db.session.delete(t)
            db.session.commit()
            return jsonify({'message': 'OK'}), 200
