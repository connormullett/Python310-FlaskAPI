
import json

from flask import request, g, Blueprint, json, Response
from ..shared.authentication import Auth
from ..models.blog_post import BlogPostModel, BlogPostSchema


blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogPostSchema()


@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    '''
    Creates a blog post
    '''

    req_data = request.get_json()
    req_data['owner_id'] = g.user['id']
    data, error = blogpost_schema.load(req_data)

    if error:
        print(error)
        return custom_response(error, 404)

    post = BlogPostModel(data)
    post.save()

    data = blogpost_schema.dump(post).data
    return custom_response(data, 201)


@blogpost_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    '''
    returns all blog BlogPostSchema
    '''

    posts = BlogPostModel.get_all_blogposts()
    data = blogpost_schema.dump(posts, many=True).data
    return custom_response(data, 200)


def custom_response(res, status_code):
    '''
    creates custom responses to
    api requests on blog post api
    '''

    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
