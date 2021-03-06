
from flask import Flask, jsonify
from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt
from .models import user, blog_post

from .views.user_view import user_api as user_blueprint
from .views.blog_post_view import blogpost_api as blog_blueprint


def create_app(env_name='development'):
    '''Create app context'''

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(blog_blueprint, url_prefix='/api/v1/blogpost')

    bcrypt.init_app(app)
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def health_check():
        return jsonify({'status': 'bigger success'}), 200

    return app
