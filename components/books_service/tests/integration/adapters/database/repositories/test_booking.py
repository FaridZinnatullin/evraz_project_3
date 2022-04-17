import datetime

import pytest
from attr import asdict
from components.books_service.adapters.database import tables
from components.books_service.adapters.database.repositories import BookingRepo
from components.books_service.application.dataclasses import Booking
from sqlalchemy.orm import registry

# Актуальная бронь на неделю
test_booking_1 = {
    'user_id': 1,
    'book_id': 1,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 20, 14, 56, 40, 902733),
    'redeemed': False,
    'id': 1,
}

# Бронь с истекшим сроком бронирования
test_booking_2 = {
    'user_id': 1,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17, 506412),
    'redeemed': False,
    'id': 2,
}

test_booking_3 = {
    'user_id': 2,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17, 506412),
    'redeemed': False,
    'id': 3,
}


@pytest.fixture(scope='function')
def fill_booking_db(session):
    session.execute(tables.booking.insert(), [test_booking_1, test_booking_2, test_booking_3])


@pytest.fixture(scope='function')
def mapping():
    mapper = registry()
    mapper.map_imperatively(Booking, tables.booking)


@pytest.fixture(scope='function')
def booking_repo(transaction_context):
    return BookingRepo(context=transaction_context)


def test__get_by_id(booking_repo, fill_booking_db):
    booking = booking_repo.get_by_id(booking_id=test_booking_1['id'])

    assert asdict(booking) == test_booking_1


def test__get_by_book_id(booking_repo, fill_booking_db):
    booking = booking_repo.get_by_book_id(book_id=test_booking_1['book_id'])

    assert asdict(booking) == test_booking_1


def test__get_by_user_id(booking_repo, fill_booking_db):
    booking = booking_repo.get_by_user_id(user_id=test_booking_3['user_id'])

    assert asdict(booking) == test_booking_3


def test__check_book_available_true(booking_repo, fill_booking_db):
    result_bool = booking_repo.check_book_available(book_id=test_booking_1['book_id'])

    assert result_bool


def test__check_book_available_false(booking_repo, fill_booking_db):
    result_bool = booking_repo.check_book_available(book_id=test_booking_2['book_id'])

    assert not result_bool


def test__get_all(booking_repo, fill_booking_db):
    bookings = booking_repo.get_all()

    assert [asdict(booking) for booking in bookings] == [test_booking_1, test_booking_2, test_booking_3]


def test__get_users_booking(booking_repo, fill_booking_db):
    bookings = booking_repo.get_users_booking(test_booking_1['user_id'])

    assert [asdict(booking) for booking in bookings] == [test_booking_1, test_booking_2]
