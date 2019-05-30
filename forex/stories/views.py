from flask import Blueprint, request, jsonify, make_response
from .models import Story, StorySchema, get_stories

stories = Blueprint('stories', __name__, url_prefix='/stories')


@stories.route('/')
def index():
    count = request.args.get('count', 10)

    stories = get_stories(count)
    stories_schema = StorySchema(many=True)
    result = stories_schema.dump(stories)
    return jsonify({'data': result.data})
