import pytest
from attr import asdict
from pydantic import ValidationError

from components.books_service.application import errors, services


@pytest.fixture(scope='function')
def service_book(books_repo, publisher):
    return services.BooksManager(books_repo=books_repo, publisher=publisher)


data_book = {
    'id': 1001605784161,
    'title': 'Coffee Break Python Slicing',
    'subtitle': '24 Workouts to Master Slicing in Python, Once and for All',
    'price': 0.00,
    'rating': 0,
    'authors': 'Christian Mayer',
    'publisher': 'Self-publishing',
    'year': 2018,
    'pages': 89,
    'desc': 'Puzzle-based learning is an active learning technique. With code puzzles, you will learn faster, smarter, and better.Coffee Break Python Slicing is all about growing your Python expertise - one coffee at a time. The focus lies on the important slicing technique to access consecutive data ranges. Und...',
    'service_tag': 'python',
    'batch_datetime': '15.04.2022 17:59:44',
    'redeemed': False,
    'booking_datetime': '25.04.2022 17:59:44'
}

data_book_1 = {
    'id': 9781118678640,
    'title': 'Windows Azure Web Sites',
    'subtitle': '',
    'price': 4.50,
    'rating': 0,
    'authors': 'James Chambers',
    'publisher': 'Wrox',
    'year': 2013,
    'pages': 120,
    'desc': 'If you are looking for a straightforward, practical...',
    'service_tag': 'azure',
    'batch_datetime': '15.04.2022 17:59:44',
    'redeemed': False,
    'booking_datetime': '25.04.2022 17:59:44'
}


def test_get_book(service_book):
    book = service_book.get_book_by_id(book_id=1001605784161)
    assert asdict(book) == data_book


def test_get_book_missing_id(service_book):
    with pytest.raises(ValidationError):
        service_book.get_book_by_id()


def test_get_book_uncorrected_params(service_book, books_repo):
    books_repo.get_by_id.return_value = None
    book_id = 0

    with pytest.raises(errors.UncorrectedParams):
        service_book.get_book_by_id(book_id=book_id)


def test_get_all_books(service_book):
    books = service_book.get_all_books()
    assert [asdict(book) for book in books] == [data_book, data_book_1]


def test_get_all_books_uncorrected(service_book, books_repo):
    books_repo.get_all.return_value = None

    with pytest.raises(errors.UncorrectedParams):
        service_book.get_all_books()

def test_get_book_from_service_uncorrected_params(service_book):
    tags = []
    with pytest.raises(errors.UncorrectedParams):
        service_book.get_book_from_service(tags)
