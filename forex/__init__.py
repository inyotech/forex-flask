from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Configuration')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    cors.init_app(app)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from forex.api import api

    app.register_blueprint(api)

    return app
