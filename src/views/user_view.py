
from flask import request, json, Response, Blueprint
from ..models.user import UserModel, UserSchema
from ..share.Authentication import Auth


 user_api = Blueprint('users', __name__)
 user_schema = UserSchema()


@user_api.route('/', mehtods=['POST'])
def create():
    '''
    Create endpoint for user api
    '''

    req_data = requests.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    # check if user already exists in db
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user in db:
        message = {'error': 'User already exists, please supply another email address'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'token': token}, 201)


def custom_response(res, status_code):
    '''
    Creates a custom json response
    for proper status messages
    '''

    return response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
