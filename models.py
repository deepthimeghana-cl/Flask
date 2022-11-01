from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from flask_migrate import Migrate

app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class BooksModel(db.Model) :
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer(), unique=True, nullable=False)
    book_name = db.Column(db.String(80), nullable=False)

    def __init__(self, book_id, book_name) :
        self.book_id = book_id
        self.book_name = book_name

    def __repr__(self) :
        return f"{self.book_id}:{self.book_name}"