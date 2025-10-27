import pytest
from django.core.exceptions import ValidationError
from backend.models import Book

@pytest.mark.django_db
def test_cannot_delete_author_with_books(author, publisher, genre):
    Book.objects.create(
        title="A Book",
        author=author,
        publisher=publisher,
        genre=genre,
        description="desc",
        price="5.00",
        publication_date="2020-01-01",
        isbn="3333333333333",
        stock=1
    )
    with pytest.raises(ValidationError):
        author.delete()