
from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .models import user, blog_post

from .views.user_view import user_api as user_blueprint


def create_app(env_name='development'):
    '''Create app context'''

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

    bcrypt.init_app(app)
    db.init_app(app)


    @app.route('/', methods=['GET'])
    def index():
        '''example endpoint'''
        return 'Test Successful'

    return app
