#!/usr/bin/env python3

import os

from src.app import create_app
from flask_heroku import Heroku


if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV')
    app = create_app(env_name)
    heroku = Heroku(app)
    app.run()
