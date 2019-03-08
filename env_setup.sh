#!/usr/bin/zsh

export FLASK_ENV='development'
export DATABASE_URL='postgres://$USER@localhost/api_blog_db'
export JWT_SECRET_KEY='supersecretkey'

