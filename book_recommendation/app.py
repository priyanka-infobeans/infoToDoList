from book_app import app,db
from flask import Flask, request, jsonify
from book_app.models import Books

# Route to get book and its reviews by book_id
@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book_and_reviews(book_id):
    book = Books.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book.to_dict())

# Route to get all books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = Books.query.all()
    return jsonify([book.to_dict() for book in books])

# Route to add a new book using POST request
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json  # Assuming the request contains data in JSON format
    new_book = Books(
        title=data['title'],
        author=data['author'],
        category=data['category'],
        rating=data['rating'],
        summary=data['summary'],
        image=data['image']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201  # Return the newly added book with HTTP status code 201 Created

# Route to delete a book by its ID using DELETE request
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Books.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

# API endpoint to update a book
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Get the book data from the request JSON
    data = request.json

    # Retrieve the book from the database
    book = Books.query.get(book_id)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    # Update the book properties
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'category' in data:
        book.category = data['category']
    if 'rating' in data:
        book.rating = data['rating']
    if 'summary' in data:
        book.summary = data['summary']
    if 'image' in data:
        book.image = data['image']

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Book updated successfully"}), 200