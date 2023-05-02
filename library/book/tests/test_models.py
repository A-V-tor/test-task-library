from book.models import Book, Author
import pytest


@pytest.fixture
def new_book(db):
    return Book.objects.create(title='Test', description='test')


def test_create_book(new_book):
    assert new_book.title == 'Test'


def test_update_book(new_book):
    book_id = new_book.id
    new_book.title = 'new title'
    new_book.save()
    up_book = Book.objects.filter(id=book_id).first()
    assert up_book.title == 'new title'


def test_delete_book(new_book):
    book_id = new_book.id
    new_book.delete()
    check = Book.objects.filter(id=book_id).first()
    assert check is None
