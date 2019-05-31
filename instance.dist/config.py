import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.dirname(__file__)}/db.sqlite3'
