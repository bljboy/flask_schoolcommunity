# 数据库配置消息
SECRET_KEY = "sdfadsfdgdsafs/fs"
HOST = 'bljboy.itdage.cn'
PORT = '3306'
DATABASE = 'schoolcommunity'
USERNAME = 'schoolcommunity'
PASSWORD = 'bljboy'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
