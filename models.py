from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship, backref

from flask import Flask
import os
from flask_migrate import Migrate

app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

Base = declarative_base()

class BooksModel(db.Model) :
    __tablename__ = "Books"
    book_id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    author = relationship("AuthorsModel", backref="BooksModel")
    location = relationship("LocationModel", backref=backref("BooksModel", uselist=False))
    readers = relationship("ReaderModel", secondary="ReaderBook")

    def __init__(self, book_id, book_name) :
        self.book_id = book_id
        self.book_name = book_name

    def __repr__(self) :
        return f"{self.book_id}:{self.book_name}"

class AuthorsModel(db.Model) :
    __tablename__ = "Authors"
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(80), nullable=False)
    book_id = db.Column(db.Integer(), ForeignKey("Books.book_id"))

    def __init__(self, author_name, book_id) :
        self.book_id = book_id
        self.author_name = author_name

    def __repr__(self) :
        return f"{self.author_name}:{self.book_id}"

class LocationModel(db.Model) :
    __tablename__ = "Location"
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(80), nullable=False)
    book_id = db.Column(db.Integer(), ForeignKey("Books.book_id"))

    def __init__(self, location_name, book_id) :
        self.book_id = book_id
        self.location_name = location_name

    def __repr__(self) :
        return f"{self.location_name}:{self.book_id}"

class ReaderModel(db.Model) :
    __tablename__ = "Readers"
    reader_id = db.Column(db.Integer(), primary_key=True)
    reader_name = db.Column(db.String(80), nullable=False)
    book = relationship("BooksModel", secondary="ReaderBook")

    def __init__(self, reader_id, reader_name) :
        self.reader_id = reader_id
        self.reader_name = reader_name

    def __repr__(self) :
        return f"{self.reader_name}:{self.reader_id}"

class ReaderBookModel(db.Model) :
    __tablename__ = "ReaderBook"
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer(), ForeignKey("Readers.reader_id"))
    book_id = db.Column(db.Integer(), ForeignKey("Books.book_id"))
    reader = relationship(ReaderModel, backref=backref("ReaderModel", cascade="all, delete-orphan"))
    book = relationship(BooksModel, backref=backref("BooksModel", cascade="all, delete-orphan"))

    #def __init__(self, reader_id, book_id) :
    #    self.reader_id = reader_id
    #    self.book_id = book_id

    def __repr__(self) :
        return f"{self.reader_id}:{self.book_id}"
