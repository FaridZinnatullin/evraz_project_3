from evraz.classic.app.errors import AppError


class NoPermission(AppError):
    msg_template = "You have no permissions to perform this action"
    code = 'books.no_permissions'


class bookAlreadyExist(AppError):
    msg_template = "This login is already occupied"
    code = 'books.book_already_exist'


class UncorrectedParams(AppError):
    msg_template = "You give me very bad params... I have no data for you"
    code = 'books.bad_params'


class Bannedbook(AppError):
    msg_template = "This book was banned in this chat"
    code = 'books.banned_book'


class UncorrectedLoginPassword(AppError):
    msg_template = "Incorrect bookname or password"
    code = 'books.authorization'


class BookIsUnavailable(AppError):
    msg_template = "Sorry, but book is unavailable"
    code = 'books.unavailable'


class BookAlreadyExist(AppError):
    msg_template = "Book already exist"
    code = 'book.already exist'


class BookingIsUnavailable(AppError):
    msg_template = "The booking time has expired or the booking has been deleted"
    code = 'booking.unavailable'
