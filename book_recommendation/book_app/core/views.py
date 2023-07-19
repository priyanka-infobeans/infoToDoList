from flask import render_template,request,Blueprint,jsonify,redirect,flash,url_for
from book_app.models import Books,Review,ReviewForm
from book_app import db

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    form = ReviewForm()
    # Get the page number from the request query parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of books to display per page

    # Paginate the books query
    books_data = Books.query.paginate(page=page, per_page=per_page)
    return render_template('index.html',books=books_data, form=form)

@core.route('/info')
def info():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('info.html')

@core.route('/books')
def book_list():
    # Get the search query, category, and author from the request query parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    author_filter = request.args.get('author', '').strip()

    # Get the sorting option from the request query parameters
    sort_by = request.args.get('sort', 'best')  # Default to 'best'

    # Get the page number from the request query parameters
    page = request.args.get('page', 1, type=int)
    per_page = 4  # Number of books to display per page

    # Filter the books based on the search query and filter
    books_data = Books.query

    if search_query:
        # Filter by book name (title) using ILIKE to perform a case-insensitive search
        books_data = books_data.filter(Books.title.ilike(f'%{search_query}%'))

    if category_filter:
        # Filter by category using ILIKE to perform a case-insensitive search
        books_data = books_data.filter(Books.category.ilike(f'%{category_filter}%'))

    if author_filter:
        # Filter by author using ILIKE to perform a case-insensitive search
        books_data = books_data.filter(Books.author.ilike(f'%{author_filter}%'))

    # Sort the books based on the sorting option
    if sort_by == 'best':
        books_data = books_data.order_by(Books.rating.desc())
    elif sort_by == 'latest':
        books_data = books_data.order_by(Books.id.desc())
    elif sort_by == 'old':
        books_data = books_data.order_by(Books.id.asc())

    # Paginate the books query
    books_data = books_data.paginate(page=page, per_page=per_page)

    return render_template('books_list.html', books=books_data)

# API endpoint to fetch categories and authors
@core.route('/api/categories_and_authors')
def get_categories_and_authors():
    # Get distinct categories and authors from the database
    categories = [result[0] for result in db.session.query(Books.category.distinct())]
    authors = [result[0] for result in db.session.query(Books.author.distinct())]

    return jsonify({"categories": categories, "authors": authors})


# Route to display book details page
@core.route("/books/<int:book_id>", methods=["GET", "POST"])
def book_details(book_id):
    # Get the book based on the book_id
    book = Books.query.get_or_404(book_id)
    print('hi')
    # Get the reviews for the specific book
    reviews = Review.query.filter_by(book_id=book_id).all()
    print(reviews)

    if book is None:
        # Handle the case when the book is not found
        flash('Book not found.', 'error')
        return redirect(url_for('core.book_list'))

    if request.method == "POST":
        # Get review data from the form
        rating = int(request.form["rating"])
        review_text = request.form["review_text"]

        # Create a new review object and associate it with the book
        review = Review(rating=rating, review=review_text, book=book)

        # Add the review to the database
        db.session.add(review)
        db.session.commit()

        # Redirect back to the book detail page with the updated review
        return redirect(url_for("book_details", book_id=book_id))

    return render_template("book_details.html", book=book, reviews=reviews)

@core.route('/submit_review', methods=['POST'])
def submit_review():
    # Get the form data from the AJAX request
    data = request.get_json()

    # Extract the review data
    book_id = data.get('book_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    # Create a new Review object and add it to the database
    review = Review(book_id=book_id, rating=rating, review=review_text)
    db.session.add(review)
    db.session.commit()

    # Return a response to indicate the review was submitted successfully
    return jsonify({'message': 'Review submitted successfully'})