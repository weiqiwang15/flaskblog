from datetime import datetime
from hashlib import md5
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

from app import db, bcrypt, login_manager
from app.models.role import Permission, Role


class User(UserMixin, db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    signature = db.Column(db.String(140))
    about_me = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    post_comments = db.relationship('PostComment', backref='author', lazy='dynamic')
    post_comment_replies = db.relationship('PostCommentReply', backref='author', lazy='dynamic')
    # thoughts = db.relationship('Thought', backref='author', lazy='dynamic')
    # thought_comments = db.relationship('ThoughtComment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError('密码不是一个可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def can(self, permission):
        return self.role is not None and self.role.has_permission(permission)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def default_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        u = 'https://cn.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        return u

    def gravatar_hash(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://cn.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url,
            hash=hash,
            size=size,
            default=default,
            rating=rating,
        )

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permission):
        return False

    def is_administrator(self):
        return False



