# from datetime import datetime
#
# from app import db
#
#
# class Thought(db.Model):
#
#     __tablename__ = 'Thoughts'
#
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     time_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     time_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     comments = db.relationship('ThoughtComment', backref='thought', lazy='dynamic')
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def __repr__(self):
#         return '<Thought {0}>'.format(self.body)
