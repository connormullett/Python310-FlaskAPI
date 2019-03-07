#!/usr/bin/env python3.7

import os

from src.app import create_app


if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV')
    app = create_app(env_name)
    app.run()
