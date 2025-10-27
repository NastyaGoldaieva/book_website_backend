import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from backend.models import Book, Author, Publisher, Genre

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="Password123")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def author(db):
    return Author.objects.create(name="Author 1")

@pytest.fixture
def publisher(db):
    return Publisher.objects.create(name="Publisher 1")

@pytest.fixture
def genre(db):
    return Genre.objects.create(name="Fiction")

@pytest.fixture
def book(db, author, publisher, genre):
    return Book.objects.create(
        title="Sample Book",
        author=author,
        publisher=publisher,
        genre=genre,
        description="Sample description",
        price="9.99",
        publication_date="2020-01-01",
        isbn="1234567890123",
        stock=5
    )

@pytest.fixture
def valid_book_payload(author, publisher, genre):
    return {
        "title": "New Book",
        "author": author.id,
        "publisher": publisher.id,
        "genre": genre.id,
        "description": "Nice book",
        "price": "15.50",
        "publication_date": "2024-01-01",
        "isbn": "9876543210123",
        "stock": 10
    }

@pytest.fixture
def invalid_book_payload():
    return {
        "title": "",
        "author": None,
        "publisher": None,
        "genre": None,
        "description": "",
        "price": "abc",
        "publication_date": "invalid-date",
        "isbn": "badisbn",
        "stock": -5
    }