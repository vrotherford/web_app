# -*- coding: UTF-8 -*-
from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(48))
    password = db.Column(db.String(48))
    groups_fk = db.Column(db.Integer)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Films(db.Model):
    __tablename__ = 'Films'
    id = db.Column(db.Integer, primary_key = True)
    caption = db.Column(db.String(48))
    year = db.Column(db.Integer)
    director = db.Column(db.String(45))
    length = db.Column(db.Integer)
    country = db.Column(db.String(45))
    g_id = db.Column(db.Integer, db.ForeignKey('Genre.id'))
    genre = db.relationship('Genre', primaryjoin="Films.g_id == Genre.id")

    def __init__(self, id = None, caption = None, year = 0, director = 'Н/И', lenght = 0, country = None, genre_id = 1):
        self.id = id
        self.caption = caption
        self.year = year
        self.director =director
        self.length = lenght
        self.country = country
        self.g_id = genre_id

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key = True)
    caption = db.Column(db.String(45))