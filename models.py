from datetime import datetime

from exts import db


# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中
# app.py必须导入from models import Jkyw


# 邮箱验证表
# class EmailCaptchaModel(db.Model):
#     __tablename__ = "email_captcha"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(100), nullable=False)
#     captcha = db.Column(db.String(100), nullable=False)


# 用户表
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class JkywModel(db.Model):
    __tablename__ = "jkyw"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(10), nullable=False, unique=True)
    jkyw_page = db.Column(db.Text, nullable=False)
