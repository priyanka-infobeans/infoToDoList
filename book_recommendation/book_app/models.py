from book_app import db,login_manager,app
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
from flask import Flask, render_template, request, redirect, url_for


# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

# Book model
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    rating = db.Column(db.Float)
    summary = db.Column(db.Text)
    image = db.Column(db.String(255))  # Add the 'image' attribute for book images

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'rating': self.rating,
            'summary': self.summary
           # 'reviews': [review.to_dict() for review in self.reviews]
        }

class ReviewForm(FlaskForm):
    rating = DecimalField('Rating', validators=[InputRequired()])
    review = TextAreaField('Review', validators=[InputRequired()])
    submit = SubmitField('Submit Review')

# Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)

    book_id = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'review': self.review,
        }

# Create the database tables within the application context
with app.app_context():
    db.create_all()
