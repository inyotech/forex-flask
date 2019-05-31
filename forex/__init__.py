import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from forex import commands


db = SQLAlchemy()
cors = CORS()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Configuration')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    cors.init_app(app)

    from forex.rates.views import rates
    from forex.stories.views import stories

    app.register_blueprint(rates)
    app.register_blueprint(stories)

    app.cli.add_command(commands.test)
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.load_currencies)
    app.cli.add_command(commands.load_rates)
    app.cli.add_command(commands.load_stories)

    return app
