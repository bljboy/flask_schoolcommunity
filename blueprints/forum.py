from flask import Blueprint, jsonify

from blueprints.forms import ReplyForm
from exts import db

from flask import request

from models import UserModel, ForumModel, ReplyModel

bp = Blueprint('forum', __name__, url_prefix='/forum')


@bp.route('/forum_all', methods=['GET'])
def forum_all():
    res = ForumModel.query.all()
    data = []
    for post in res:
        data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'email': post.user.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "获取成功", "data": data})


@bp.route('/myforum/delete', methods=['GET'])
def myforum_delete():
    id = request.args.get("id")
    res = ForumModel.query.get(id)
    db.session.delete(res)
    db.session.commit()
    return jsonify({"code": 200, "message": "删除成功", "data": None})


@bp.route('/myforum', methods=['GET'])
def myforum_query():
    email = request.args.get("email")
    res = ForumModel.query.order_by(ForumModel.join_time.desc()).filter_by(email_id=email).all()
    data = []
    for post in res:
        data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'email': post.user.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "获取成功", "data": data})


@bp.route("/reply/content")
def qa_detail():
    forum_id = request.args.get('forum_id')
    replies = ReplyModel.query.order_by(ReplyModel.join_time.desc()).filter_by(forum_id=forum_id).all()
    data = []
    for post in replies:
        data.append({
            'content': post.content,
            'email': post.user.email,
            'time': post.join_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return jsonify({"code": 200, "message": "成功", "data": data})


@bp.route('/reply', methods=['POST'])
def reply():
    email = request.form.get('email')
    content = request.form.get('content')
    forum_id = request.form.get('forum_id')
    reply_data = ReplyModel(content=content, forum_id=forum_id, user_id=email)
    # reply_data = ReplyModel(content=content, forum_id=forum_id, user_id=user_id)
    db.session.add(reply_data)
    db.session.commit()
    return 'ok'


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
