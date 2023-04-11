from flask import Blueprint, json, request, jsonify
from flask_socketio import join_room, emit

from exts import mail, db, socketio

bp = Blueprint('chat', __name__, url_prefix='')


@socketio.on('connect')
def on_connect():
    print('客户端已连接')


@socketio.on('message')
def handle_message(data):
    # 发送消息到特定房间
    print(data)
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data['content']
    room = get_room_id(sender_id, receiver_id)
    join_room(room)
    emit('message', {'sender_id': sender_id, 'receiver_id': receiver_id, 'content': content}, room=room)
    return content


def get_room_id(sender_id, receiver_id):
    # 将两个用户名按照字典序排序
    sorted_names = sorted([sender_id, receiver_id])
    user1_name = sorted_names[0]
    user2_name = sorted_names[1]
    # 根据用户名创建唯一的房间 ID
    return 'room_{}_{}'.format(user1_name, user2_name)
# @socketio.on('connect')
# def on_connect():
#     print('客户端已连接')
#     join_room('chatroom')
#
#
# @socketio.on('message')
# def handle_message(data):
#     print('收到消息：', data)
#     sender_id = data['sender_id']
#     receiver_id = data['receiver_id']
#     content = data['content']
#     emit('message', {'sender_id': sender_id, 'receiver_id': receiver_id, 'content': content}, room='chatroom')
#     return content
