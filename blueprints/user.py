from flask import Blueprint, request, jsonify
from sqlalchemy import not_

from models import UserModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/query_all', methods=['GET'])
def query():
    email = request.args.get("email")
    all_users = UserModel.query.filter(not_(UserModel.email == email)).all()
    data = []
    for post in all_users:
        data.append({
            'id': post.id,
            'email': post.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "成功", "data": data})
