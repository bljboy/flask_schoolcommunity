from flask import Blueprint
from flask_socketio import join_room, emit

from exts import mail, db, socketio

bp = Blueprint('chat', __name__, url_prefix='')


@bp.route('/')
def index():
    print("chat")
    return "chat"


@socketio.on('connect')
def on_connect():
    print('客户端已连接')
    join_room('chatroom')


@socketio.on('message')
def handle_message(data):
    print('收到消息：', data)
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data['content']
    emit('message', {'sender_id': sender_id, 'receiver_id': receiver_id, 'content': content}, room='chatroom')
    return content
