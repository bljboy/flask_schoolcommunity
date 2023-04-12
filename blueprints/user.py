from flask import Blueprint, request, jsonify
from sqlalchemy import not_

from exts import db
from models import UserModel, ReplyModel, ForumModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/delete_all', methods=['GET'])
def user_delete():
    email = request.args.get("email")
    user = UserModel.query.filter(UserModel.email == email).first()
    forum = ForumModel.query.filter_by(email_id=user.email).all()
    reply = ReplyModel.query.filter_by(user_id=user.email).all()
    for f in forum:
        db.session.delete(f)
    for r in forum:
        db.session.delete(r)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"code": 200, "message": "删除成功", "data": None})


@bp.route('/user_all', methods=['GET'])
def user_all():
    all_users = UserModel.query.all()
    data = []
    for post in all_users:
        data.append({
            'id': post.id,
            'email': post.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "成功", "data": data})


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
