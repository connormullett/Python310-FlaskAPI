
from . import db
from datetime import datetime

from marshmallow import fields, Schema


class BlogPostModel(db.Model):
    '''
    BlogPost Model
    '''

    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        '''
        Takes in a json request body
        as data and parses to
        instance attributes
        '''

        self.owner_id = data.get('owner_id')
        self.title = data.get('title')
        self.content = data.get('content')
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return f'<id {self.id}>'

    def delete(self):
        '''
        deletes current model from database
        '''
        db.session.delete(self)
        db.session.commit()

    def save(self):
        '''
        saves new object to database
        '''
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        '''
        updates model after setting attributes
        and persists them to database
        '''
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return BlogPostModel.query.all()

    @staticmethod
    def get_one_blogpost(id):
        return BlogPostModel.query.get(id)


class BlogPostSchema(Schema):
  """
  Blogpost Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  content = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
