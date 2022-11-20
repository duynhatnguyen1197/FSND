from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()
database_path = os.environ.get('DATABASE_URL')
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    release_date = db.Column(db.DateTime())
    casts = db.relationship('Cast',cascade="all,delete",backref='movie',lazy='joined')
    is_delete = db.Column(db.Boolean)
    
    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def short_form(self):
        return {
        'title': self.title,
        'release_date': self.release_date.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()



class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean)
    casts = db.relationship('Cast',cascade="all,delete",backref='actor',lazy='joined')

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }

    def short_form(self):
        return {
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    

class Cast(db.Model):
    __tablename__ = 'Cast'

    id = db.Column(db.Integer, primary_key=True)
    is_delete = db.Column(db.Boolean)
    movie_id = db.Column(db.Integer,db.ForeignKey('Movie.id'),nullable=False)
    actor_id = db.Column(db.Integer,db.ForeignKey('Actor.id'),nullable=False)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()