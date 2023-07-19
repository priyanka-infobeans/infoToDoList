import csv
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from book_app import app, db
from book_app.models import Books

def main():
    with app.app_context():
        f = open("books.csv")
        reader = csv.reader(f)
        for name, price, description,author in reader:
            book = Books(name=name, price=price, description=description, author=author)
            db.session.add(book)
            print(f"Added book {name}, {price}, {description}")
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)