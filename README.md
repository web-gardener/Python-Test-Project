# Flask Bookstore Application

## Overview
This Flask application serves as a simple bookstore, allowing users to add books, search for books, and view book history.

## Prerequisites
- Python 3.x
- Flask
- SQLite

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Database Setup
1. Create a SQLite database file named `books.db`.
2. Run the Flask application to create the necessary tables:
   ```bash
   python app.py
   
## Running the Application
1. Start the Flask application:
   ```bash
   python app.py
2. Open your web browser and navigate to http://localhost:5000/ping to check if the application is running.

## Endpoints
- `/ping`: Ping endpoint to check if the application is running.
- `/author`: POST endpoint to add a new author.
- `/author/<int:key>`: GET endpoint to get author details by ID.
- `/book`: POST endpoint to add a new book.
- `/book/<int:key>`: GET endpoint to get book details by ID.
- `/book?barcode=<barcode>`: GET endpoint to search for books by barcode.
- `/leftover`: POST endpoint to add leftover information.
- `/history/<int:key>`: GET endpoint to get book history by ID.

## Usage Examples
- Adding a new author:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "birth_date": "1990-01-01"}' http://localhost:5000/author
- Add a new book:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"barcode": "12345", "title": "Example Book", "publish_year": 2022, "author_id": 1}' http://localhost:5000/book
- Getting book details by ID:
  ```bash
  curl http://localhost:5000/book/1
