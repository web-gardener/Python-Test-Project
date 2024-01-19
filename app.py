# app.py
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

class Storing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('storing_info', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())


# Ping endpoint
@app.route('/ping')
def ping():
    return jsonify({"message": "pong"}), 200

# Authors endpoints
@app.route('/author', methods=['POST'])
def add_author():
    data = request.json

    if not all(key in data for key in ('name', 'birth_date')):
        return jsonify({"message": "Wrong request structure"}), 422

    new_author = Author(**data)
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"key": new_author.id}), 201

@app.route('/author/<int:key>', methods=['GET'])
def get_author(key):
    try: 
        author = Author.query.get(key)

        return jsonify({"key": author.id, "name": author.name}), 200
    except:
        return jsonify({"message": "Entity not found"}), 404

# Books endpoints
@app.route('/book', methods=['POST'])
def add_book():
    data = request.json

    if not all(key in data for key in ('barcode', 'title', 'publish_year', 'author_id')):
        return jsonify({"message": "Wrong request structure"}), 422

    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"key": new_book.id}), 201

@app.route('/book/<int:key>', methods=['GET'])
def get_book(key):
    try:
        book = Book.query.get(key)

        result = {
            "key": book.id,
            "barcode": book.barcode,
            "title": book.title,
            "publish_year": book.publish_year,
            "author": {"name": book.author.name, "birth_date": book.author.birth_date},
            "quantity": book.storing_info[-1].quantity if book.storing_info else 0
        }
        return jsonify(result), 200
    except:
        return jsonify({"message": "Entity not found"}), 404


@app.route('/book', methods=['GET'])
def search_book():
    barcode = request.args.get('barcode')
    books = Book.query.filter_by(barcode=barcode).order_by(Book.barcode).all()

    result = {
        "found": len(books),
        "items": [
            {
                "key": book.id,
                "barcode": book.barcode,
                "title": book.title,
                "publish_year": book.publish_year,
                "author": {"name": book.author.name, "birth_date": book.author.birth_date},
                "quantity": book.storing_info[-1].quantity if book.storing_info else 0
            } for book in books
        ]
    }
    return jsonify(result), 200

# Storing endpoints
@app.route('/leftover', methods=['POST'])
def add_leftover():
    data = request.json

    if not all(key in data for key in ('book_id', 'quantity')):
        return jsonify({"message": "Wrong request structure"}), 422

    new_leftover = Storing(**data)
    db.session.add(new_leftover)
    db.session.commit()
    return jsonify({"key": new_leftover.id}), 201

@app.route('/history/<int:key>', methods=['GET'])
def get_history(key):
    try: 
        book = Book.query.get(key)

        result = {
            "book": {"key": book.id, "title": book.title},
            "history": [
                {"date": storing.date, "quantity": storing.quantity} for storing in book.storing_info
            ]
        }
        return jsonify(result), 200
    except:
        return jsonify({"message": "Entity not found"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
