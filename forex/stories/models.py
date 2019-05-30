import datetime, dateutil

from marshmallow import Schema, fields

from forex import db

# table classes

class Story(db.Model):

    __tablename__ = 'stories'

    id             = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title          = db.Column(db.String(255), nullable=False)
    description    = db.Column(db.Text(), nullable=False)
    link           = db.Column(db.String(255), nullable=False)
    feed_url       = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.DateTime(), nullable=False)
    created_date   = db.Column(db.DateTime(), nullable=False)


# serialization classes

class StorySchema(Schema):
    class Meta:
        fields = ('title', 'description', 'link', 'feed_url', 'published_date', 'created_date')


# query functions

def get_stories(count=10):
    return db.session.query(
        Story
    ).order_by(db.func.random()).limit(count) \
     .from_self().order_by(Story.published_date.desc()).all()
