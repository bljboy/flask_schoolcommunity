from flask import Flask

from flask_migrate import Migrate

import config
from blueprints.chat import bp as chat
from blueprints.user import bp as user
from blueprints.search import bp as search
from blueprints.forum import bp as forum
from blueprints.email_login import bp as email_login
from blueprints.jkyw import bp as jkyw
from exts import db, mail, socketio

app = Flask(__name__)
# 配置json编码
app.config['JSON_AS_ASCII'] = False

# 绑定配置文件
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
socketio.init_app(app)
migrate = Migrate(app, db)

# blueprint；用来做模块化的
app.register_blueprint(jkyw)
app.register_blueprint(email_login)
app.register_blueprint(forum)
app.register_blueprint(search)
app.register_blueprint(chat)
app.register_blueprint(user)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, **{'allow_unsafe_werkzeug': True})
