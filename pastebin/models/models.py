import hashlib, urllib
from hashlib import md5
from flask import request
from pastebin.models import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    photo = db.Column(db.String(64), nullable=True, unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    api_key = db.Column(db.String(64), nullable=True, unique=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))

    def gravatar(self, size=100, default='wavatar', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class Pastes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255), index=True)
    paste = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime())
    date_timelive = db.Column(db.DateTime())
    private = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    code_id = db.Column(db.Integer(), db.ForeignKey('codelanguages.id'), default=1)

    users = db.relationship('User', backref='pastes')

    def __repr__(self):
        return self.title


class Codelanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, default=True)

    pastes = db.relationship('Pastes', backref='codelanguages')
