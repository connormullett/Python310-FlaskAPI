#!/usr/bin/env python3

import os

from src.app import create_app
from flask_heroku import Heroku

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
heroku = Heroku(app)

if __name__ == '__main__':
    app.run()

