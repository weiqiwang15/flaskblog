from datetime import datetime

from app import db


class PostComment(db.Model):

    __tablename__ = 'PostComments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    time_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))
    replies = db.relationship('PostCommentReply', backref='comment', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<PostComment {0}>'.format(self.body)


class PostCommentReply(db.Model):

    __tablename__ = 'PostCommentReplies'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    time_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('PostComments.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<PostCommentReply {0}>'.format(self.body)


# class ThoughtComment(db.Model):
#
#     __tablename__ = 'ThoughtComments'
#
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     time_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     time_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     disabled = db.Column(db.Boolean, default=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     thought_id = db.Column(db.Integer, db.ForeignKey('Thoughts.id'))
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def __repr__(self):
#         return '<ThoughtComment {0}>'.format(self.body)
