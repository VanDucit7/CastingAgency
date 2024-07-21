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


def create_data_test():
    db.drop_all()
    db.create_all()
    # movie Tom And Jerry
    movie1 = Movie(title="Tom And Jerry", release_date="06/27/2024 18:31:00")
    movie1.insert()

    actor1 = Actor(name="Tom", age=3, gender=Gender.MALE.value)
    actor1.movies.append(movie1)
    actor1.insert()

    actor2 = Actor(name="Jerry", age=2, gender=Gender.FEMALE.value)
    actor2.movies.append(movie1)
    actor2.insert()

    # movie Conan
    movie2 = Movie(title="Conan", release_date="07/28/2024 13:09:00")
    movie2.insert()

    actor3 = Actor(name="Shinichi", age=18, gender=Gender.MALE.value)
    actor3.movies.append(movie2)
    actor3.insert()

    actor4 = Actor(name="Ran", age=18, gender=Gender.FEMALE.value)
    actor4.movies.append(movie2)
    actor4.insert()

    # movie Doreamon
    movie3 = Movie(title="Doreamon", release_date="05/26/2024 10:35:00")
    movie3.insert()

    actor5 = Actor(name="Nobita", age=7, gender=Gender.MALE.value)
    actor5.movies.append(movie3)
    actor5.insert()

    actor6 = Actor(name="Doreamon", age=7, gender=Gender.MALE.value)
    actor6.movies.append(movie3)
    actor6.insert()

    actor7 = Actor(name="Xuka", age=7, gender=Gender.MALE.value)
    actor7.movies.append(movie3)
    actor7.insert()


# ROUTES


movie_actor = db.Table('movie_actor',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                       db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
                       )


# class MovieActor(db.Model):
#     __tablename__ = 'movie_actor'
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
#     actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)
#
#     def __init__(self, movie_id, actor_id):
#         self.movie_id = movie_id
#         self.actor_id = actor_id
#
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def update(self):
#         db.session.commit()
#
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    actors = db.relationship('Actor', secondary=movie_actor, lazy='subquery',
                             backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        actors = [actor.format_no_movie() for actor in self.actors]
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': actors
        }

    def format_no_actors(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movies = [movie.format_no_actors() for movie in self.movies]
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': movies
        }

    def format_no_movie(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Gender(Enum):
    NOT_KNOWN = 0
    MALE = 1
    FEMALE = 2
    NOT_APPLICABLE = 9
