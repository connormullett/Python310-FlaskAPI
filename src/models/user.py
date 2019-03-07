
import datetime
from marshmallow import fields, schema

from . import db
from ..app import bcrypt

class UserModel(db.Model):
    '''
    User Model
    __tablename__ defines the
    database tables name on migration
    class attributes are for declaring
    the database columns
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        '''
        takes in a json request body
        and parses to instance attributes
        '''

        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<id {self.id}>'

    def _generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def delete(self):
        '''deletes row from db'''
        db.session.delete(self)

    def save(self):
        '''saves current state of model to db'''
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        '''takes in data to modify model'''
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
