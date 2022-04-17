import datetime

import pytest
from attr import asdict
from components.books_service.application import errors, services


@pytest.fixture(scope='function')
def service_booking(booking_repo, books_repo, publisher):
    return services.BookingManager(
        booking_repo=booking_repo, books_repo=books_repo, publisher=publisher
    )


# Актуальная бронь на неделю
data_booking = {
    'user_id': 1,
    'book_id': 1,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 20, 14, 56, 40, 902733),
    'redeemed': False,
    'id': 1,
}

# Бронь с истекшим сроком бронирования
data_booking_1 = {
    'user_id': 1,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17, 506412),
    'redeemed': False,
    'id': 1,
}

data_booking_2 = {
    'user_id': 2,
    'book_id': 2,
    'created_datetime': datetime.datetime(2022, 4, 10, 14, 56, 40, 902733),
    'expiry_datetime': datetime.datetime(2022, 4, 14, 12, 35, 17, 506412),
    'redeemed': False,
    'id': 3,
}


def test_get_by_id(service_booking):
    book = service_booking.booking_repo.get_by_id(booking_id=data_booking['id'])
    assert asdict(book) == data_booking


def test_get_by_id_uncorrected_params(service_booking, booking_repo):
    booking_id = 9999
    booking_repo.get_by_id.return_value = None

    with pytest.raises(errors.UncorrectedParams):
        service_booking.get_by_id(booking_id=booking_id)


def test_get_by_book_id(service_booking):
    booking = service_booking.booking_repo.get_by_book_id(
        book_id=data_booking['book_id']
    )
    assert asdict(booking) == data_booking


def test_get_by_user_id(service_booking):
    booking = service_booking.booking_repo.get_by_user_id(
        user_id=data_booking['user_id']
    )
    assert asdict(booking) == data_booking


def test_get_active_booking(service_booking):
    booking = service_booking.get_active_booking(
        user_id=data_booking['user_id']
    )
    assert asdict(booking) == data_booking


def test_get_active_booking_overdude_booking(service_booking, booking_repo):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_user_id.return_value = overdude_booking

    with pytest.raises(errors.UserNoActiveBooking):
        service_booking.get_active_booking(user_id=data_booking['user_id'])


def test_get_active_booking_redeemed(service_booking, booking_repo):
    redeemed_booking = booking_repo.get_redeemed_booking()
    booking_repo.get_by_user_id.return_value = redeemed_booking

    with pytest.raises(errors.UserNoActiveBooking):
        service_booking.get_active_booking(user_id=data_booking['user_id'])


def test_check_book_available(service_booking, booking_repo):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_user_id.return_value = overdude_booking
    booking_repo.get_by_book_id.return_value = overdude_booking

    result = service_booking.check_book_available(
        book_id=data_booking['book_id'], user_id=data_booking['user_id']
    )
    assert result == True


def test_check_book_available_user_already_have_booking(
    service_booking, booking_repo
):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_book_id.return_value = overdude_booking

    with pytest.raises(errors.UserAlreadyHaveBooking):
        service_booking.check_book_available(
            book_id=data_booking['book_id'], user_id=data_booking['user_id']
        )


def test_check_book_available_book_already_booked(
    service_booking, booking_repo
):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_user_id.return_value = overdude_booking

    with pytest.raises(errors.BookAlreadyBooked):
        service_booking.check_book_available(
            book_id=data_booking['book_id'], user_id=data_booking['user_id']
        )


def test_check_book_available_uncorrected_params(service_booking, books_repo):
    books_repo.get_by_id.return_value = None

    with pytest.raises(errors.UncorrectedParams):
        service_booking.check_book_available(
            book_id=data_booking['book_id'], user_id=data_booking['user_id']
        )


def test_check_permission_positive(service_booking):
    assert service_booking.check_permission(
        booking_id=data_booking['id'], user_id=data_booking['user_id']
    ) == True


def test_check_permission_negative(service_booking):
    booking_id = 3
    user_id = 3
    assert service_booking.check_permission(
        user_id=user_id, booking_id=booking_id
    ) == None


def test_booking_book(service_booking, booking_repo):
    period = 7
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_user_id.return_value = overdude_booking
    booking_repo.get_by_book_id.return_value = overdude_booking

    service_booking.booking_book(
        book_id=data_booking['book_id'],
        user_id=data_booking['user_id'],
        period=period
    )

    service_booking.booking_repo.add_instance.assert_called_once()


def test_booking_book_without_period(service_booking, booking_repo):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_user_id.return_value = overdude_booking
    booking_repo.get_by_book_id.return_value = overdude_booking

    service_booking.booking_book(
        book_id=data_booking['book_id'], user_id=data_booking['user_id']
    )

    service_booking.booking_repo.add_instance.assert_called_once()


def test_booking_book_negative(service_booking, booking_repo):
    period = 7

    with pytest.raises(errors.UserAlreadyHaveBooking):
        service_booking.booking_book(
            book_id=data_booking['book_id'],
            user_id=data_booking['user_id'],
            period=period
        )


def test_delete_booking(service_booking, booking_repo):
    service_booking.delete_booking(
        booking_id=data_booking['id'], user_id=data_booking['user_id']
    )
    service_booking.booking_repo.add_instance.assert_called_once()


def test_delete_booking_uncorrected_params(service_booking, booking_repo):
    booking_repo.get_by_id.return_value = None

    with pytest.raises(errors.UncorrectedParams):
        service_booking.delete_booking(
            booking_id=data_booking['id'], user_id=data_booking['user_id']
        )


def test_delete_booking_book_unavailable(service_booking, booking_repo):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_id.return_value = overdude_booking

    with pytest.raises(errors.BookingIsUnavailable):
        service_booking.delete_booking(
            booking_id=data_booking['id'], user_id=data_booking['user_id']
        )


def test_redeem_booking(service_booking, booking_repo):
    service_booking.redeem_booking(
        booking_id=data_booking['id'], user_id=data_booking['user_id']
    )

    service_booking.booking_repo.add_instance.assert_called_once()


def test_redeem_booking_no_permission(service_booking, booking_repo):
    with pytest.raises(errors.NoPermission):
        service_booking.redeem_booking(
            booking_id=data_booking_2['id'], user_id=data_booking_2['user_id']
        )


def test_redeem_booking_booking_unavailable(service_booking, booking_repo):
    overdude_booking = booking_repo.get_overdude_booking()
    booking_repo.get_by_id.return_value = overdude_booking

    with pytest.raises(errors.BookingIsUnavailable):
        service_booking.redeem_booking(
            booking_id=data_booking['id'], user_id=data_booking['user_id']
        )


def test_get_all_users_booking(service_booking):
    bookings = service_booking.get_all_users_booking(
        user_id=data_booking['user_id']
    )

    assert [asdict(booking)
            for booking in bookings] == [data_booking, data_booking_1]
