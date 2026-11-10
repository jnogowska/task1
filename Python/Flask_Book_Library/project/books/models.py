
from project import db, app
from sqlalchemy.orm import validates
import re


# Input validation - task 2
def validate_book_text(value, field_name, required=False):
    if not isinstance(value, str):
        raise ValueError(f"{field_name} musi byc tekstem")

    value = value.strip()

    if required and not value:
        raise ValueError(f"{field_name} nie moze byc puste")

    if len(value) > 64:
        raise ValueError(f"{field_name} moze miec maksymalnie 64 znaki")

    if "<" in value or ">" in value:
        raise ValueError(f"{field_name} zawiera niedozwolone znaki HTML")

    return value


# Book model
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    # Input validation when assigning values to the model
    @validates("name", "author")
    def validate_text_fields(self, key, value):
        return validate_book_text(
            value,
            key,
            required=(key == "name")
        )

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
