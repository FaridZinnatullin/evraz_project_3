from evraz.classic.app.errors import AppError


class NoPermission(AppError):
    msg_template = "You have no permissions to perform this action"
    code = 'books.no_permissions'


class bookAlreadyExist(AppError):
    msg_template = "This login is already occupied"
    code = 'books.book_already_exist'


class UncorrectedParams(AppError):
    msg_template = "Wa have no data with yours parameters"
    code = 'books.bad_params'


class UncorrectedLoginPassword(AppError):
    msg_template = "Incorrect bookname or password"
    code = 'books.authorization'


class BookIsUnavailable(AppError):
    msg_template = "Sorry, but book is unavailable"
    code = 'books.unavailable'


class BookAlreadyExist(AppError):
    msg_template = "Book already exist"
    code = 'book.already exist'


class BookAlreadyBooked(AppError):
    msg_template = "This book is already booked"
    code = 'book.already_booked'


class BookingIsUnavailable(AppError):
    msg_template = "The booking time has expired or the booking has been deleted"
    code = 'booking.unavailable'


class UserAlreadyHaveBooking(AppError):
    msg_template = "Sorry, but you cannot have more than one active booking"
    code = 'user.already_have_booking'


class UserNoActiveBooking(AppError):
    msg_template = "This user has no active bookings"
    code = 'user.no_active_booking'
