from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# import sqlite3

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE,"
#                " author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

app = Flask(__name__)
# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)


# Define Book class
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# # Create the books table in the database
# with app.app_context():
#     db.create_all()
#
# # Modify the existing book in the database
# with app.app_context():
#     book = Book.query.filter_by(id=1).first()
#     book.title = 'Harry Potter and the Philosopher\'s Stone'
#     book.author = 'J.K. Rowling'
#     book.rating = 9.3
#     db.session.commit()

# all_books = []


def edit_rating(book_id, new_rating):
    with app.app_context():
        book = Book.query.filter_by(id=book_id).first()
        book.rating = new_rating
        db.session.commit()


def delete(book_id):
    with app.app_context():
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()

    return render_template("index.html", all_books=all_books, delete_book=delete_book)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book_title = request.form.get("title")
        author_name = request.form.get("author")
        book_rating = request.form.get("rating")

        # Add a book to the database
        with app.app_context():
            book = Book(title=book_title, author=author_name, rating=book_rating)
            db.session.add(book)
            db.session.commit()

        return redirect(url_for('home'))

        # all_books.append(
        #     {
        #         "Book Title": book_title,
        #         "Author Name": author_name,
        #         "Book Rating": book_rating,
        #     }
        # )
        # print(all_books)

    return render_template("add.html")


@app.route("/change_rating/<int:book_id>", methods=["POST", "GET"])
def change_rating(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_title = book.title
    book_author = book.author
    book_rating = book.rating

    if request.method == "POST":
        book_new_rating = request.form[f"{book_title}_new_rating"]
        edit_rating(book_id, book_new_rating)
        return redirect(url_for('home'))

    return render_template(
        "change_rating.html",
        book_id=book_id,
        book_title=book_title,
        book_author=book_author,
        book_rating=book_rating
    )


@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    delete(book_id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
