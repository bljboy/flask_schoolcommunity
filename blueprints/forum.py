from flask import Blueprint, jsonify

from exts import db

from flask import request

from models import UserModel, ForumModel
from datetime import datetime

bp = Blueprint('forum', __name__, url_prefix='/forum')



# def favorite():
#     favorite = FavoriteModel(title=forum.title, forum_id=forum.id, email=email)
#     db.session.add(favorite)
#     db.session.commit()
#     return jsonify({'message': 'Favorite added successfully'})


@bp.route('/', methods=['GET'])
def query():
    posts = db.session.query(ForumModel).order_by(ForumModel.join_time.desc()).all()
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'email': post.user.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "获取成功", "data": data})


# @bp.route('/', methods=['GET'])
# def query():
#     email = request.args.get('email')
#     user = UserModel.query.filter_by(email=email).first()
#     if not user:
#         print(email)
#         return jsonify({"code": 200, "meassage": "账号出现问题", "data": None})
#     else:
#         posts = db.session.query(ForumModel).join(UserModel).filter_by(email=email).all()
#         data = []
#         for post in posts:
#             data.append({
#                 'id': post.id,
#                 'title': post.title,
#                 'content': post.content,
#                 'email': post.user.email
#             })
#         return jsonify({"code": 200, "message": "获取成功", "data": data})


@bp.route('/push', methods=['POST'])
def push():
    if request.method == 'GET':
        return 'GET请求错误'
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        email = request.form.get('email')
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            print(email)
            return jsonify({"code": 200, "meassage": "账号出现问题", "data": None})
        else:
            post = ForumModel(title=title, content=content, email_id=email)
            db.session.add(post)
            db.session.commit()
            return jsonify({"code": 200, "meassage": "发布成功", "data": None})
