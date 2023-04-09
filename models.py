from datetime import datetime

import pytz

from exts import db


# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中
# app.py必须导入from models import Jkyw

# # 收藏模型
# class FavoriteModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Integer, db.ForeignKey('forum.title'), nullable=False)
#     forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
#     email = db.Column(db.String(100), db.ForeignKey('forum.email_id'), nullable=False)

# 帖子
class ForumModel(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    email_id = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    user = db.relationship('UserModel', backref=db.backref('posts', lazy=True))
    join_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')),
                          nullable=False)


# 邮箱验证表
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)  # 邮箱验证表


# 用户表
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # favorites = db.relationship('FavoriteModel', backref='user', lazy=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class JkywModel(db.Model):
    __tablename__ = "jkyw"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(10), nullable=False, unique=True)
    jkyw_page = db.Column(db.Text, nullable=False)
