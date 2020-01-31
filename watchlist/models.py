# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db

class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.nickname


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Comment(db.Model):
    
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    news_id = db.Column(db.String(255))
    post_time = db.Column(db.String(255))
    content = db.Column(db.String(10000))
    like_count = db.Column(db.Integer)
    rank_a = db.Column(db.Integer, default=  0)
    rank_b = db.Column(db.Integer, default=  0)
    rank_c = db.Column(db.Integer, default=  0)
    rank = db.Column(db.Integer, default=  0)




class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
