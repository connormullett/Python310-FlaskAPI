
import jwt
import os
import datetime

from functools import wraps

from flask import json, Response, request, g
from ..models.user import UserModel


class Auth:
    '''
    Auth handles authentication and
    creation of json webtokens
    for user model
    '''

    @staticmethod
    def auth_required(f):
        '''
        decorator similar to @login_required
        '''

        @wraps(f)
        def auth_wrapper(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype='application/json',
                    response=json.dumps({
                        'error': 'Authentication token not provided'
                    }),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype='application/json',
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)

            if not check_user:
                return Response(
                    mimetype='application/json',
                    response=json.dumps({
                        'error': 'user does not exist, bad token'
                    }),
                    status=400
                )

            g.user = {'id': user_id}
            return f(*args, **kwargs)
        return auth_wrapper


    @staticmethod
    def decode_token(token):
        '''
        Takes in a JW Token and validates
        it against the JWT library with
        the secret key
        '''

        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as el:
            re['error'] = {'message': 'invalid token'}
            return re

    @staticmethod
    def generate_token(user_id):
        '''
        Creates a json web token for a user
        '''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode('utf-8')
        except Exception as e:
            return Response(
                mimetype='application/json',
                response=json.dumps({'error': 'error generating user token'}),
                status=400
            )
