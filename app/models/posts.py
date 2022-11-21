from app import db
from datetime import datetime
from wtforms import ValidationError

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        json_post={
            'post_id':self.id,
            'body':self.body,
            'timestamp':self.timestamp,
            'author_id':self.user_id
        }
        return json_post

    def from_json(json_post):
        body=json_post.get('body')
        if body is None or body=='':
            raise ValidationError('El post no tiene contenido')
        return Posts(body=body)

    def __repr__(self):
        return '<Post {}>'.format(self.body)