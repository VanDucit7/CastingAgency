from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime
from settings import DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL
import os

database_name = DB_NAME
# database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, 'localhost:5432', database_name)
# database_path = DATABASE_URL
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
create database to test
"""


# ROUTES


book_history = db.Table('book_history',
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                       db.Column('history_id', db.Integer, db.ForeignKey('history.id'))
                       )

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    numberOfPages = db.Column(db.Integer)
    photo = db.Column(db.String)
    createDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    histories = db.relationship('History', secondary=book_history, lazy='subquery',
                             backref=db.backref('books', lazy=True))

    def __init__(self, name, author, numberOfPages, photo, createDate):
        self.name = name
        self.author = author
        self.numberOfPages = numberOfPages
        self.photo = photo
        self.createDate = createDate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        histories = [history.format_no_book() for history in self.histories]
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'numberOfPages': self.numberOfPages,
            'photo': self.photo,
            'createDate': self.createDate,
            'histories': histories
        }

    def format_no_history(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'numberOfPages': self.numberOfPages,
            'photo': self.photo,
            'createDate': self.createDate
        }


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    fromPage = db.Column(db.Integer)
    toPage = db.Column(db.Integer)
    tag = db.Column(db.String)
    createDate = db.Column(db.DateTime, nullable=False, default
