import pytest
from attr import asdict
from sqlalchemy.orm import registry

from components.books_service.adapters.database import tables
from components.books_service.adapters.database.repositories import BookRepo
from components.books_service.application.dataclasses import Book

test_book_1 = {
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
    'batch_datetime': '15.04.2022 17:59:44'
}

test_book_2 = {
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
    'batch_datetime': '15.04.2022 17:59:44'
}


@pytest.fixture(scope='function')
def fill_book_db(session):

    session.execute(tables.books.insert(), [test_book_1, test_book_2])


@pytest.fixture(scope='function')
def mapping():
    mapper = registry()
    mapper.map_imperatively(Book, tables.books)


@pytest.fixture(scope='function')
def book_repo(transaction_context):
    return BookRepo(context=transaction_context)


def test__get_by_id(book_repo, fill_book_db):
    book = book_repo.get_by_id(book_id=test_book_1['id'])

    assert asdict(book) == test_book_1


def test__get_all(book_repo, fill_book_db):
    books = book_repo.get_all()

    assert len(books) != 0
    assert [asdict(book) for book in books] == [test_book_1, test_book_2]


def test__add_instance_package(book_repo, fill_book_db):
    books_data = [Book(**book_data) for book_data in [test_book_1, test_book_2]]
    books = book_repo.add_instance_package(books_data)

    assert books == None


def test__delete_by_id(book_repo, fill_book_db):
    result = book_repo.delete_by_id(test_book_1['id'])

    assert result == None


def test__get_by_name_author(book_repo, fill_book_db):
    book = book_repo.get_by_name_author(author=test_book_1['authors'],
                                        name=test_book_1['title'])

    assert asdict(book) == test_book_1


def test__get_books_with_filters(book_repo, fill_book_db):
    filtering_params = {
        'keyword': ['Python'],
        'publisher': ['Self-publishing']
    }
    books = book_repo.get_books_with_filters(params=filtering_params,
                                             sorting_key='price')

    assert books[0] == test_book_1['id']


def test__get_top_by_tag(book_repo, fill_book_db):
    tag = test_book_1['service_tag']
    batch_datetime = test_book_1['batch_datetime']
    books = book_repo.get_top_by_tag(tag, batch_datetime)

    assert asdict(books[0]) == test_book_1

def test__add_instance(book_repo, mapping):
    book_data = Book(**test_book_1)
    book = book_repo.add_instance(book_data)

    assert asdict(book) == test_book_1
