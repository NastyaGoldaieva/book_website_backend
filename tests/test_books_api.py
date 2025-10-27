import pytest
from rest_framework import status
from backend.models import Book

LIST_URL = "/api/books/"
def detail_url(pk): return f"/api/books/{pk}/"

@pytest.mark.django_db
def test_list_books_public(api_client, book):
    res = api_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)

@pytest.mark.django_db
def test_list_books_filters_and_sort(auth_client, author, publisher, genre):
    Book.objects.create(
        title="Alpha Book",
        author=author,
        publisher=publisher,
        genre=genre,
        description="A",
        price="5.00",
        publication_date="2022-01-01",
        isbn="1111111111111",
        stock=1
    )
    Book.objects.create(
        title="Beta Book",
        author=author,
        publisher=publisher,
        genre=genre,
        description="B",
        price="10.00",
        publication_date="2023-01-01",
        isbn="2222222222222",
        stock=2
    )
    res = auth_client.get(LIST_URL, {"title": "Alpha"})
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert any("Alpha Book" == b["title"] for b in data)
    res2 = auth_client.get(LIST_URL, {"sort": "price_asc"})
    assert res2.status_code == status.HTTP_200_OK
    prices = [float(b["price"]) for b in res2.json()]
    assert prices == sorted(prices)

@pytest.mark.django_db
def test_retrieve_book_requires_auth(api_client, book):
    url = detail_url(book.id)
    res = api_client.get(url)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_retrieve_book_authenticated(auth_client, book):
    url = detail_url(book.id)
    res = auth_client.get(url)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data.get("id") == book.id
    assert "author_name" in data and data["author_name"] == book.author.name
    assert "publisher_name" in data and data["publisher_name"] == book.publisher.name
    assert "genre_name" in data and data["genre_name"] == book.genre.name

@pytest.mark.django_db
def test_post_to_books_not_allowed(api_client, valid_book_payload):
    res = api_client.post(LIST_URL, data=valid_book_payload, format="json")
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.django_db
def test_put_delete_on_book_not_allowed(auth_client, book, valid_book_payload):
    url = detail_url(book.id)
    res_put = auth_client.put(url, data=valid_book_payload, format="json")
    res_delete = auth_client.delete(url)
    assert res_put.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert res_delete.status_code == status.HTTP_405_METHOD_NOT_ALLOWED