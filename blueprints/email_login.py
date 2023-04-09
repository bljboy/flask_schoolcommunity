from flask import Blueprint, render_template, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from blueprints.forms import RegisterForm, LoginForm
from exts import mail, db
from flask_mail import Message
from flask import request, render_template, jsonify, redirect, url_for
import string
import random
from models import EmailCaptchaModel
from models import UserModel

bp = Blueprint('email_login', __name__, url_prefix='/email_login')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'GET请求错误'
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("不存在")
                form = RegisterForm(request.form)
                if form.validate():
                    email = form.email.data
                    user = UserModel(email=email)
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({"code": 200, "meassage": "注册成功", "data": None})
                else:
                    print(form.errors)
                    return form.errors
            else:
                res_form = RegisterForm(request.form)
                if res_form.validate():
                    return jsonify({"code": 200, "meassage": "登录成功", "data": None})
                else:
                    print(res_form.errors)
                    return res_form.errors
        else:
            print(form.errors)
            return form.errors


# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     # 验证用户提交的邮箱和验证码是否在对应且正确
#     if request.method == 'GET':
#         return 'GET请求错误'
#     else:
#         form = RegisterForm(request.form)
#         if form.validate():
#             email = form.email.data
#             user = UserModel(email=email)
#             db.session.add(user)
#             db.session.commit()
#             return "ok"
#         else:
#             print(form.errors)
#             return form.errors


@bp.route('/captcha')
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # email = request.form.get('email')
    # 4/6:随机产生数字，字母，数字和字母的组合
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    message = Message(subject="论坛注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    # memcached/redis
    # 用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code:200/400/500,message:"",data:{}}
    return jsonify({"code": 200, "meassage": "获取成功", "data": None})


@bp.route('/test')
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2371076453@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"
