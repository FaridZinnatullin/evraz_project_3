import datetime
from unittest.mock import Mock

import pytest
from falcon import testing

from components.books_service.adapters import books_api
from components.books_service.application import services, dataclasses


@pytest.fixture(scope='function')
def book():
    return dataclasses.Book(
        id=1001605784161,
        title='Coffee Break Python Slicing',
        subtitle='24 Workouts to Master Slicing in Python, Once and for All',
        price=0.00,
        rating=0,
        authors='Christian Mayer',
        publisher='Self-publishing',
        year=2018,
        pages=89,
        desc='Puzzle-based learning is an active learning technique. With code puzzles, you will learn faster, smarter, and better.Coffee Break Python Slicing is all about growing your Python expertise - one coffee at a time. The focus lies on the important slicing technique to access consecutive data ranges. Und...',
        service_tag='python',
        batch_datetime='15.04.2022 17:59:44',
        redeemed=False,
        booking_datetime='25.04.2022 17:59:44'
    )


@pytest.fixture(scope='function')
def book_1():
    return dataclasses.Book(
        id=9781118678640,
        title='Windows Azure Web Sites',
        subtitle='',
        price=4.50,
        rating=0,
        authors='James Chambers',
        publisher='Wrox',
        year=2013,
        pages=120,
        desc='If you are looking for a straightforward, practical...',
        service_tag='azure',
        batch_datetime='15.04.2022 17:59:44',
        redeemed=False,
        booking_datetime='25.04.2022 17:59:44'
    )


# Актуальная бронь на неделю
@pytest.fixture(scope='function')
def booking():
    return dataclasses.Booking(
        user_id=1,
        book_id=1,
        created_datetime=datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
        expiry_datetime=datetime.datetime(2022, 4, 20, 14, 56, 40, 902733),
        redeemed=False,
        id=1,
    )


# Бронь с истекшим сроком бронирования
@pytest.fixture(scope='function')
def booking_1():
    return dataclasses.Booking(
        user_id=1,
        book_id=2,
        created_datetime=datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
        expiry_datetime=datetime.datetime(2022, 4, 14, 12, 35, 17, 506412),
        redeemed=False,
        id=2,
    )


# Выкупленная бронь
@pytest.fixture(scope='function')
def booking_2():
    return dataclasses.Booking(
        user_id=2,
        book_id=1,
        created_datetime=datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
        expiry_datetime=datetime.datetime(2080, 4, 20, 14, 56, 40, 902733),
        redeemed=True,
        id=1,
    )


@pytest.fixture(scope='function')
def books_service(book, book_1):
    books_service = Mock(services.BooksManager)
    books_service.get_book_by_id = Mock(return_value=book)
    books_service.get_all_books = Mock(return_value=[book, book_1])
    books_service.filter_books = Mock(return_value=[book_1])
    return books_service


@pytest.fixture(scope='function')
def books_updater_service(book, book_1):
    books_updater_service = Mock(services.BooksManager)
    books_updater_service.get_all_users = Mock(return_value=None)
    return books_updater_service


@pytest.fixture(scope='function')
def booking_service(booking, booking_1, booking_2):
    booking_service = Mock(services.BooksManager)
    booking_service.get_all_users = Mock(return_value=None)
    booking_service.booking_book = Mock(return_value=None)
    booking_service.get_by_id = Mock(return_value=booking)
    booking_service.get_all_users_booking = Mock(return_value=[booking, booking_1])
    booking_service.delete_booking = Mock(return_value=None)
    booking_service.redeem_booking = Mock(return_value=None)
    booking_service.get_active_booking = Mock(return_value=booking)

    return booking_service


@pytest.fixture(scope='function')
def client(books_service, books_updater_service, booking_service):
    app = books_api.create_app(
        booking_manager=booking_service,
        books_updater=books_updater_service,
        books_manager=books_service,
    )

    return testing.TestClient(app)
