from exts import db


# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中
# app.py必须导入from models import Jkyw

class JkywModel(db.Model):
    __tablename__ = "jkyw"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(10), nullable=False, unique=True)
    jkyw_page = db.Column(db.Text, nullable=False)
