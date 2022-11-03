from flask import Flask
from flask import render_template, redirect
from flask import request
from models import db, app, BooksModel
from flask_migrate import Migrate

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home() :
    if request.form :
        book = BooksModel(book_name=request.form.get("book_name"), book_id=request.form.get("book_id"))
        print(request.form)
        db.session.add(book)
        db.session.commit()
    return redirect("/books")

@app.route("/books")
def home_read() :
    books = BooksModel.query.all()
    for book in books:
        print(book.book_id)
        print(book.book_name)
    return render_template("home.html", books=books)

@app.route("/books/<int:id>")
def SingleBook(id) :
    book = BooksModel.query.filter_by(book_id=id).first()
    print(book)
    if book :
        return render_template('book.html', book=book)
    return f"Book with ID={id} doesn't exist"

@app.route("/books/<int:id>/update",  methods=["GET", "POST"])
def update(id) :
    book = BooksModel.query.filter_by(book_id=id).first()
    print(book)
    if request.method == "POST" :
        if book :
           return render_template("update.html", book=book)
        return f"Book with id = {id} doesn't exist"
    return "Do Nothing?"

@app.route("/books/<int:id>/updated", methods=["GET", "POST"])
def updated(id) :
    book = BooksModel.query.filter_by(book_id=id).first()
    if request.method == "POST" :
        if book :
            book_id = book.book_id
            db.session.delete(book)
            db.session.commit()
            #id = request.form.get("book_id")
            name = request.form.get("book_name")
            book_new = BooksModel(book_id=book_id, book_name=name)
            print(book_new)
            db.session.add(book_new)
            db.session.commit()
            return redirect(f'/books')
        return f"Book with id = {id} doesn't exist"
    return redirect(f'/books/{id}')

@app.route("/books/<int:id>/delete")
def deleted(id) :
    book = BooksModel.query.filter_by(book_id=id).first()
    if request.method == "POST" :
        if book :
            book_id = book.book_id
            db.session.delete(book)
            db.session.commit()
            return redirect(f'/books')
        return f"Book with id = {id} doesn't exist"
    return redirect(f'/books/{id}')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)