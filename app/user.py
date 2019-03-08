from app import api
from flask import request
from app.model import Student

@api.route('/users/myself', methods=['PUT', 'GET'])
def myself():
    if request.method == 'PUT':
        pass
