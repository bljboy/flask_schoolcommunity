from flask import Blueprint, jsonify
from flask import request
from sqlalchemy_searchable import make_searchable, search

from models import ForumModel

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/')
def search_all():
    content = request.args.get("content");
    result = ForumModel.query.filter(ForumModel.content.like(f"%{content}%")).all()
    data = []
    for forum in result:
        post = {
            'id': forum.id,
            'title': forum.title,
            'content': forum.content,
            'email': forum.email_id,
            'time': forum.join_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        data.append(post)
    return jsonify({"code": 200, "message": "成功", "data": data})
