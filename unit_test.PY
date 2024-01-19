import unittest
import json
from app import app, db, Book, Author

class TestBookEndpoints(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book_valid_data(self):
        with app.app_context():
            author = Author(name="John Doe", birth_date="2000-01-01")
            db.session.add(author)
            db.session.commit()

            response = self.app.post('/book', json={"title": "Test Book", "publish_year": 2022, "author_id": author.id, "barcode": '12345'})
            self.assertEqual(response.status_code, 201)

            book = Book.query.first()
            self.assertEqual(book.title, "Test Book")

    def test_get_book_existing_id(self):
        with app.app_context():
            author = Author(name="Jane Doe", birth_date="1995-05-05")
            db.session.add(author)
            db.session.commit()

            book = Book(title="Another Book", publish_year=2021, author_id=author.id)
            db.session.add(book)
            db.session.commit()

            response = self.app.get(f'/book/{book.id}')
            self.assertEqual(response.status_code, 200)

            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data["key"], book.id)

if __name__ == '__main__':
    unittest.main()
