import os

from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import api
    app.register_blueprint(api.bp)

    from . import websocket
    websocket.setup_websocket_routes(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
