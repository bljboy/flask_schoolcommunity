from flask import Blueprint
from flask import request
from flask_mail import Message

from blueprints.forms import RegisterForm
from exts import mail, db

bp = Blueprint('email_login', __name__, url_prefix='/email_login')


@bp.route('/', methods=['GET','POST'])
def email_login():
    if request.method == 'GET':
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            return form.errors
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            return form.errors


@bp.route('/test')
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2371076453@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"
