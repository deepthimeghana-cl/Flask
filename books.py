from flask import Flask
from flask import render_template, redirect
from flask import request
from models import db, app, BooksModel, AuthorsModel, LocationModel
from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home() :
    if request.form :
        book = BooksModel(book_name=request.form.get("book_name"), book_id=request.form.get("book_id"))
        author = AuthorsModel(author_name=request.form.get("author_name"), book_id=request.form.get("book_id"))
        location = LocationModel(location_name=request.form.get("location_name"), book_id=request.form.get("book_id"))
        print(request.form)
        db.session.add(book)
        db.session.commit()
        db.session.add(author)
        db.session.commit()
        db.session.add(location)
        db.session.commit()
    return redirect("/books")

@app.route("/books")
def home_read() :
    books = db.session.query(BooksModel, AuthorsModel, LocationModel).join(AuthorsModel, BooksModel.book_id == AuthorsModel.book_id)\
        .join(LocationModel, BooksModel.book_id == LocationModel.book_id).all()
    for book in books:
        print(book[0].book_id)
        print(book[0].book_name)
        print(book[1].author_name)
        print(book[2].location_name)
    return render_template("home.html", data=books)

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

@app.route("/books/<int:id>/delete", methods=["GET", "POST"])
def deleted(id) :
    book = BooksModel.query.filter_by(book_id=id).first()
    if request.method == "POST" :
        if book :
            db.session.delete(book)
            db.session.commit()
            return redirect(f'/books')
        return f"Book with id = {id} doesn't exist"
    return redirect(f'/books/{id}')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)