from flask import Flask

from flask_migrate import Migrate
from models import JkywModel
import config
from blueprints.jkyw import bp as jkyw
from exts import db

app = Flask(__name__)
# 配置json编码
app.config['JSON_AS_ASCII'] = False
# 绑定配置文件
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)

# blueprint；用来做模块化的
app.register_blueprint(jkyw)

if __name__ == '__main__':
    app.run(debug=True)
