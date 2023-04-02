from flask import Flask

from flask_migrate import Migrate
import config
from blueprints.email_login import bp as email_login
from blueprints.jkyw import bp as jkyw
from exts import db, mail

app = Flask(__name__)
# 配置json编码
app.config['JSON_AS_ASCII'] = False
# 绑定配置文件
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# blueprint；用来做模块化的
app.register_blueprint(jkyw)
app.register_blueprint(email_login)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
